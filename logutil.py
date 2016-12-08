# -*- coding: utf-8 -*-
import datetime
import logging

import os


def get_logger(asin, site, type):
    filename = "./logs/{}-{}-{}-{}.log".format(asin, site[site.rfind('.') + 1:].upper(), type, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        filename=filename,
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return logging
