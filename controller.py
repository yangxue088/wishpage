# -*- coding: utf-8 -*-
import json

from flask import Flask, request
from flask import render_template
from werkzeug.exceptions import abort

import krank
from kinventory import check_product_inventory
from kmail import send_mail_message
from kmatch import KMatch
from kthief import find_chief

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', dict=None)


@app.route('/relevance')
def relevance():
    return render_template('relevance.html', dict=None)


@app.route('/relevance/match', methods=['POST', 'GET'])
def relevance_match():
    asin = request.values.get('asin')
    site = request.values.get('site')
    asins = filter(lambda asin: len(asin) > 0, json.loads(request.values.get('asins')))
    keywords = filter(lambda keyword: len(keyword) > 0, json.loads(request.values.get('keywords')))

    data = KMatch().match(asin, site, asins, keywords)
    return json.dumps(data)


@app.route('/mail', methods=['POST', 'GET'])
def mail():
    return render_template('mail.html', dict=None)


@app.route('/mail/send', methods=['POST', 'GET'])
def mail_send():
    sender = request.values.get('sender')
    receipts = filter(lambda receipt: len(receipt) > 0, json.loads(request.values.get('receipts')))
    subject = request.values.get('subject')
    content = request.values.get('content')

    for receipt in receipts:
        try:
            send_mail_message(sender, receipt, subject, content)
            print "send mail:", receipt
        except:
            continue

    return str(len(receipts))


@app.route('/rank', methods=['POST', 'GET'])
def rank():
    return render_template('rank.html', dict=None)


@app.route('/rank/search', methods=['POST', 'GET'])
def rank_search():
    asin = request.values.get('asin')
    site = request.values.get('site')
    keywords = filter(lambda keyword: len(keyword) > 0, json.loads(request.values.get('keywords')))

    data = krank.search(asin, site, keywords)
    return json.dumps(data)


@app.route('/thief', methods=['POST', 'GET'])
def thief():
    return render_template('thief.html', dict=None)


@app.route('/thief/find', methods=['POST', 'GET'])
def thief_find():
    sites = filter(lambda site: len(site) > 0, json.loads(request.values.get('sites')))
    asins = filter(lambda asin: len(asin) > 0, json.loads(request.values.get('asins')))
    included = True if request.values.get('included') == 'true' else False

    try:
        data = find_chief(sites, asins, included)
        return json.dumps(data)
    except:
        abort(501)


@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    return render_template('inventory.html', dict=None)


@app.route('/inventory/check', methods=['POST', 'GET'])
def inventory_check():
    sites = filter(lambda site: len(site) > 0, json.loads(request.values.get('sites')))
    asins = filter(lambda asin: len(asin) > 0, json.loads(request.values.get('asins')))

    try:
        results = check_product_inventory(sites, asins)
        return json.dumps(results)
    except:
        abort(501)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
