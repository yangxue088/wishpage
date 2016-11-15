# -*- coding: utf-8 -*-
import multiprocessing
import time
import urllib2

from selenium import webdriver

import amazon


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
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)
browser.get('http://127.0.0.1:5000')
browser.maximize_window()
