# -*- coding: utf-8 -*-
import multiprocessing
import urllib2

import time
from selenium import webdriver

import controller


def start_web():
    print 'start web server...'
    controller.app.run(host='0.0.0.0', port=5000, threaded=True)
    #controller.app.run(host='127.0.0.1', port=5000, threaded=True)


if __name__ == "__main__":
    start_web()

    # multiprocessing.freeze_support()
    #
    # p = multiprocessing.Process(target=start_web)
    # p.start()
    #
    # while True:
    #     try:
    #         time.sleep(1)
    #         urllib2.urlopen('http://127.0.0.1:6000')
    #         print('test web server successful...')
    #         break
    #     except:
    #         pass
    #
    # print 'open browser to request...'
    # chrome_options = webdriver.ChromeOptions()
    # browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)
    # browser.get('http://127.0.0.1:6000/inventory')
    # browser.maximize_window()
