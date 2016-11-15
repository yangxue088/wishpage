# -*- coding: utf-8 -*-
import multiprocessing
import time

from pip._vendor import requests
from selenium import webdriver

import amazon

if __name__ == '__main__':

    def start_web():
        print 'start web server...'
        amazon.app.run(host='0.0.0.0')


    p = multiprocessing.Process(target=start_web)
    p.start()

    while True:
        time.sleep(1)
        try:
            request = requests.get('http://127.0.0.1:5000')
            if request.status_code == 200:
                print('test web server successful...')
                break
        except:
            pass

    print 'open browser to request...'
    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:5000')
