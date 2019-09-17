from flask import Flask, render_template, request, redirect, url_for, \
    send_from_directory
import requests as http_client
from http import HTTPStatus
from settings import THRESHOLD, ENDPOINT, TITLE


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


def create_app(ENDPOINT):
    app = Flask(__name__, static_url_path='/static')

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
            response = http_client.post(url=ENDPOINT, json=query)
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


if __name__ == "__main__":
    app = create_app(ENDPOINT)
    app.run(host='0.0.0.0')
