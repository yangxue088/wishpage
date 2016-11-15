# -*- coding: utf-8 -*-
import json

from flask import Flask, request
from flask import render_template

from kmatch import KMatch

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('config.html', dict=None)


@app.route('/search', methods=['POST', 'GET'])
def search():
    asin = request.values.get('asin')
    site = request.values.get('site')
    asins = filter(lambda asin: len(asin) > 0, json.loads(request.values.get('asins')))
    keywords = filter(lambda keyword: len(keyword) > 0, json.loads(request.values.get('keywords')))

    data = KMatch().match(asin, site, asins, keywords)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
