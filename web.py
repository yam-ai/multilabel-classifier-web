#!/usr/bin/env python3
# coding=utf-8
# Copyright 2019 YAM AI Machinery Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, render_template, request, redirect, url_for, \
    send_from_directory
import requests as http_client
from http import HTTPStatus
from settings import THRESHOLD, ENDPOINT, TITLE, HOST_PORT
import sys
import getopt
from urllib.parse import urlparse


def sort_dict(dct):
    lo = []
    hi = []

    for k in dct:
        if dct[k] > THRESHOLD:
            hi += [(dct[k], k)]

        else:
            lo += [(dct[k], k)]

    lo.sort(reverse=True)
    hi.sort(reverse=True)

    lo = [(j, "{:.2%}".format(i)) for (i, j) in lo]
    hi = [(j, "{:.2%}".format(i)) for (i, j) in hi]

    return lo, hi


def create_app(classifier_endpoint):
    if not classifier_endpoint:
        classifier_endpoint = ENDPOINT
    app = Flask(__name__, static_url_path='/static')
    app.logger.info('Classifier endpoint = {}'.format(classifier_endpoint))

    @app.route('/')
    def index():
        return render_template('home.html', title=TITLE)

    def error(err, info):
        app.logger.error('{}: {}'.format(err, info))

    @app.route('/ask', methods=['GET', 'POST'])
    def ask():
        passage = request.form['passage']
        query = {
            "texts": [
                {
                    "id": 0,
                    "text": passage
                }
            ]
        }
        err = None
        hi, lo = [], []
        try:
            response = http_client.post(url=classifier_endpoint, json=query)
            if response.status_code == HTTPStatus.BAD_REQUEST:
                err = 'Invalid text'
                error(err, response.text)
            elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                err = 'Internal server error'
                error(err, response.text)
            else:
                scores = response.json()[0].get("scores")
                lo, hi = sort_dict(scores)
        except Exception as e:
            err = 'Prediction service unavailable'
            error(err, e)
        app.logger.info({
            'text': passage,
            'hi': hi,
            'lo': lo
        })
        return render_template(
            'answer.html', passage=passage, title=TITLE,
            response_hi=hi, response_lo=lo, err=err)
    return app


def validate_uri(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def host_port(s):
    try:
        host, port = s.split(':')
        host = host.strip()
        return host, int(port)
    except Exception as e:
        return None, None


def quit(progname, e=None):
    m = 'Usage: {} -c classifier_endpoint -h host_port'.format(progname)
    print(m, file=sys.stderr)
    if e:
        print(e, file=sys.stderr)
    sys.exit(4)


def main(argv):
    app = None
    try:
        progname = argv[0]
        classifier_endpoint = ENDPOINT
        host, port = host_port(HOST_PORT)
        opts, _ = getopt.getopt(argv[1:], 'c:h:')
        for opt, arg in opts:
            if opt == '-c' and arg:
                classifier_endpoint = arg
                if not validate_uri(classifier_endpoint):
                    quit(progname, Exception(
                        'Invalid endpoint: {}'.format(classifier_endpoint)))
            elif opt == '-h' and arg:
                host, port = host_port(arg)
        app = create_app(classifier_endpoint)
        app.run(host=host, port=port)
    except Exception as e:
        quit(progname, e)


if __name__ == "__main__":
    main(sys.argv)
