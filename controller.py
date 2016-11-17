# -*- coding: utf-8 -*-
import json

import requests
from flask import Flask, request
from flask import render_template

from kmatch import KMatch

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('keyword.html', dict=None)


@app.route('/search', methods=['POST', 'GET'])
def search():
    asin = request.values.get('asin')
    site = request.values.get('site')
    asins = filter(lambda asin: len(asin) > 0, json.loads(request.values.get('asins')))
    keywords = filter(lambda keyword: len(keyword) > 0, json.loads(request.values.get('keywords')))

    data = KMatch().match(asin, site, asins, keywords)
    return json.dumps(data)


def send_mail_message(sender, receipt, subject, content):
    return requests.post(
        "https://api.mailgun.net/v3/tjchtech.com/messages",
        auth=("api", "key-b6139f5afd5b82a73a810724b263b380"),
        data={"from": sender,
              "to": receipt,
              "subject": subject,
              "text": content})


@app.route('/mail', methods=['POST', 'GET'])
def mail():
    return render_template('mail.html', dict=None)


@app.route('/send', methods=['POST', 'GET'])
def send_mail():
    sender = request.values.get('sender')
    receipts = filter(lambda receipt: len(receipt) > 0, json.loads(request.values.get('receipts')))
    subject = request.values.get('subject')
    content = request.values.get('content')

    for receipt in receipts:
        send_mail_message(sender, receipt, subject, content)
        print "send mail:", receipt

    return len(receipts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
