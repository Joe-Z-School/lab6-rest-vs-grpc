#!/usr/bin/env python3

from __future__ import print_function

import requests
import json
import time
import sys
import grpc
# Import files created from grpc proto file
import lab6_pb2
import lab6_pb2_grpc

import base64
import random
import argparse


def doRawImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    data = lab6_pb2.rawImageMsg(img=img)
    response = stub.rawImage(data)
    if debug:
        print("Response is", response.width, response.height)


def doAdd(stub, debug=False):
    data = lab6_pb2.addMsg(a=5, b=10)
    response = stub.add(data)
    if debug:
        print("Response is", response.sum)


def doDotProduct(stub, debug=False):
    data = lab6_pb2.dotProductMsg()
    data.a.extend([random.random() for x in range(100)])
    data.b.extend([random.random() for x in range(100)])
    response = stub.dotProduct(data)
    if debug:
        print("Response is", response.dotproduct)


def doJsonImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    data = lab6_pb2.jsonImageMsg(img=base64.b64encode(img).decode('utf-8'))
    response = stub.jsonImage(data)
    if debug:
        print("Response is", response.width, response.height)


# ---------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------

parser = argparse.ArgumentParser(
    description='gRPC client for measuring server operations'
)

parser.add_argument(
    'host',
    help='IP address or hostname of the server'
)

parser.add_argument(
    'cmd',
    choices=['add', 'rawImage', 'dotProduct', 'jsonImage'],
    help='Operation to perform'
)

parser.add_argument(
    'reps',
    type=int,
    help='Number of repetitions for measurement'
)

parser.add_argument(
    '-p', '--port',
    type=int,
    default=5000,
    help='Server port (default: 5000)'
)

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help='Print the response from the server'
)

args = parser.parse_args()


# ---------------------------------------------------------
# Build server address
# ---------------------------------------------------------

addr = f"{args.host}:{args.port}"

print(f"Running {args.reps} reps against {addr}")

# Build gRPC connection
channel = grpc.insecure_channel(addr)

# Create stub
stub = lab6_pb2_grpc.RestCompareStub(channel)


# ---------------------------------------------------------
# Perform requested operation
# ---------------------------------------------------------

if args.cmd == 'rawImage':

    start = time.perf_counter()

    for x in range(args.reps):
        doRawImage(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")


elif args.cmd == 'add':

    start = time.perf_counter()

    for x in range(args.reps):
        doAdd(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")


elif args.cmd == 'jsonImage':

    start = time.perf_counter()

    for x in range(args.reps):
        doJsonImage(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")


elif args.cmd == 'dotProduct':

    start = time.perf_counter()

    for x in range(args.reps):
        doDotProduct(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")
