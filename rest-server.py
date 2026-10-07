#!/usr/bin/env python3

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import io
import argparse

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    values = request.get_json()
    a = values['a']
    b = values['b']
    response = {'dot_product': sum(i*j for i, j in zip(a, b))}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )




@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    # Get the request data
    data = request.get_json()
    # Grab the encoded image from the data
    encodedImage = data.get('image')

    # Decode the image
    decodedImage = base64.b64decode(encodedImage)
    # Create a PIL image object
    img = Image.open(io.BytesIO(decodedImage))

    # Grab the width and height of the image
    response = {
        'width': img.size[0],
        'height': img.size[1]
    }

    # Pickle the response
    response_pickled = jsonpickle.encode(response)

    # Return the response
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
