from flask import Flask, render_template, request, redirect, url_for
import requests as http_client

THRESHOLD = 0.5

def sort_dict(dct):
    lo = []
    hi = []

    for k in dct:
        if dct[k] > THRESHOLD:
            hi += [(dct[k], k)]

        else:
            lo += [(dct[k], k)]

    lo.sort(reverse = True)
    hi.sort(reverse = True)

    lo = [(j, "{:.2%}".format(i)) for (i, j) in lo]
    hi = [(j, "{:.2%}".format(i)) for (i, j) in hi]

    return lo, hi

def create_app(ENDPOINT):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('base.html')

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
        response = http_client.post(url = ENDPOINT, json = query)

        scores = response.json()[0].get("scores")
        lo, hi = sort_dict(scores)

        return render_template('answer.html', passage = passage, response_hi = hi, response_lo = lo)

    return app

if __name__ == "__main__":
    ENDPOINT = 'http://0.0.0.0:8000/classifier'
    app = create_app(ENDPOINT)
    app.run(host='0.0.0.0')
