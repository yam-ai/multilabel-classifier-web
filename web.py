from flask import Flask, render_template, request, redirect, url_for, send_from_directory
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

    lo.sort(reverse=True)
    hi.sort(reverse=True)

    lo = [(j, "{:.2%}".format(i)) for (i, j) in lo]
    hi = [(j, "{:.2%}".format(i)) for (i, j) in hi]

    return lo, hi


def create_app(ENDPOINT):
    app = Flask(__name__, static_url_path='/static')

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/ask', methods=['GET', 'POST'])
    def ask():
        print('enter ask')
        print('form = {}'.format(request.form.to_dict()))
        passage = request.form['passage']
        print('passage = {}'.format(passage))
        query = {
            "texts": [
                {
                    "id": 0,
                    "text": passage
                }
            ]
        }
        print('query = {}'.format(query))
        response = http_client.post(url=ENDPOINT, json=query)
        print('status code = {}'.format(response.status_code))
        print('json = {}'.format(response.json()))
        scores = response.json()[0].get("scores")
        lo, hi = sort_dict(scores)

        return render_template('answer.html', passage=passage, response_hi=hi, response_lo=lo)

    return app

    # @app.route('/css/<path:path>')
    # def send_css(path):
    #     return send_from_directory('css', path)

    # @app.route('/img/<path:path>')
    # def send_img(path):
    #     return send_from_directory('img', path)


if __name__ == "__main__":
    ENDPOINT = 'http://0.0.0.0:8000/classifier'
    app = create_app(ENDPOINT)
    app.run(host='0.0.0.0')
