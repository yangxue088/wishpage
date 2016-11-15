# -*- coding: utf-8 -*-
import multiprocessing
import time
import urllib2

from selenium import webdriver

import amazon

if __name__ == '__main__':

    def start_web():
        print 'start web server...'
        amazon.app.run(host='0.0.0.0')


    p = multiprocessing.Process(target=start_web)
    p.start()

    while True:
        try:
            time.sleep(1)
            urllib2.urlopen('http://127.0.0.1:5000')
            print('test web server successful...')
            break
        except:
            pass

    print 'open browser to request...'
    browser = webdriver.Firefox()
    browser.get('http://127.0.0.1:5000')
