# -*- coding: utf-8 -*-

import httplib
import json
import urllib2
import zipfile
from collections import OrderedDict

import os
import re
from flask import Flask, request, send_file
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('search.html', dict=None)


@app.route('/download', methods=['POST', 'GET'])
def download():
    filename = request.values.get('filename')
    hrefs = request.values.get('hrefs').split(',')

    if not os.path.exists('target'):
        os.mkdir('target')

    zfilename = os.path.join('target', '{}.zip'.format(filename))
    zfile = zipfile.ZipFile(zfilename, 'w')

    try:
        for href in hrefs:
            zfile.writestr(href.split('/')[-1], urllib2.urlopen(href).read())
    finally:
        zfile.close()

    response = send_file(zfilename, as_attachment=True, attachment_filename='{}.zip'.format(filename))
    return response


@app.route('/search', methods=['POST', 'GET'])
def search():
    url = request.values.get('url')

    kvs = {}
    if url is not None:
        kvs = crawl(url)

    return render_template('search.html', dict=kvs, id=url.split('/')[-1])


def crawl(url):
    httpclient = None

    try:
        httpclient = httplib.HTTPSConnection('www.wish.com')
        httpclient.request('GET', url)
        response = httpclient.getresponse()
        return parse_response(url, response.read())
    except Exception, e:
        print e
    finally:
        if httpclient:
            httpclient.close()


def parse_response(url, body):
    kvs = OrderedDict()

    match = re.search("\['mainContestObj'\] = ({.*?});\n", body)

    if match:
        data = json.loads(match.group(1))

        kvs['卖家名称'] = data['commerce_product_info']['variations'][0]['merchant']
        kvs['卖家地址'] = 'https://www.wish.com/merchant/{}'.format(
            data['commerce_product_info']['variations'][0]['merchant_name'])
        kvs['卖家等级'] = data['commerce_product_info']['variations'][0]['merchant_rating']
        kvs['卖家评价数量'] = data['commerce_product_info']['variations'][0]['merchant_rating_count']

        kvs['产品标题'] = data['name']
        kvs['产品地址'] = url
        kvs['产品等级'] = data['product_rating']['rating']
        kvs['产品评价数量'] = data['product_rating']['rating_count']

        kvs['产品价格'] = str(data['commerce_product_info']['variations'][0]['localized_price']['localized_value']) + \
                      data['commerce_product_info']['variations'][0]['localized_price']['symbol']
        kvs['产品邮费'] = str(data['commerce_product_info']['variations'][0]['localized_shipping']['localized_value']) + \
                      data['commerce_product_info']['variations'][0]['localized_shipping']['symbol']

        kvs['产品标签'] = ', '.join(tag['name'] for tag in data['tags'])

        kvs['卖家标签'] = ', '.join(tag['name'] for tag in data['merchant_tags'])

        kvs['产品图片地址'] = sorted([photo_url.replace('small.jpg', 'origin.jpg') for photo_url in data['extra_photo_urls'].values() if
                         photo_url.endswith('small.jpg')])

        kvs['卖家评价图片'] = sorted([photo_url[:photo_url.index('&')] for photo_url in data['extra_photo_urls'].values() if
                         '&' in photo_url and '=' in photo_url])

    return kvs


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
