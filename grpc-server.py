#!/usr/bin/env python3

from concurrent import futures
import requests
import json
import time
import sys
import grpc
# Import files created from grpc proto file
import lab6_pb2
import lab6_pb2_grpc

import base64
from PIL import Image
import io
import argparse


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

class RestCompareServicer(lab6_pb2_grpc.RestCompareServicer):

    def add(self, data):
        responseA = data.a
        responseB = data.b
        reply = lab6_pb2.addReply()
        reply.sum = responseA + responseB
        return reply

    def rawimage(self, data):
        reply = lab6_pb2.imageReply()

        # Convert the data to a PIL image type so we can extract dimensions
        try:
            ioBuffer = io.BytesIO(data.img)
            img = Image.open(ioBuffer)

            reply.width = img.size[0]
            reply.height = img.size[1]
        except:
            reply.width = 0
            reply.height = 0

        return reply


    def dotproduct(self, data):
        reply = lab6_pb2.dotProductReply()
        reply.dotproduct = sum(i*j for i, j in zip(data.a, data.b))
        return reply



    def jsonimage(self, data):
        reply = lab6_pb2.imageReply()

        # Decode the image
        decodedImage = base64.b64decode(data.img)

        # Create a PIL image object
        try:
            ioBuffer = io.BytesIO(decodedImage)
            img = Image.open(ioBuffer)

            reply.width = img.size[0]
            reply.height = img.size[1]
        except:
            reply.width = 0
            reply.height = 0

        return reply

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='gRPC server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_RestCompareServicer_to_server(
        RestCompareServicer(), server
    )
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    server.wait_for_termination()
