# -*- coding: utf-8 -*-
import logging
import logging.config

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# service_args = [
#     '--proxy=127.0.0.1:1080',
#     '--proxy-type=socks5',
# ]
# browser = webdriver.PhantomJS(service_args=service_args)


def find_chief(sites, asins, included=False):
    logging.config.fileConfig('logging.conf', defaults={'type': 'thief'})
    logger = logging.getLogger('mylogger')

    our_seller = ['LIVEHITOP', 'MAIKEHIGH', 'AUTOPKIO']

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1080")
    browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)

    thieves = []
    for site in sites:
        for asin in asins:
            logger.info('check seller for site: {}, asin: {}'.format(site, asin))

            url = 'https://{}/gp/offer-listing/{}/ref=dp_olp_new_mbc'.format(site, asin)

            browser.get(url)

            while True:
                try:
                    if browser.find_element_by_id('captchacharacters'):
                        print 'wait input validate code...'
                        wait = WebDriverWait(browser, 6000)
                        wait.until(expected_conditions.invisibility_of_element_located((By.ID, "captchacharacters")))
                except:
                    break

            seller_names = list(set([link.text.strip().replace(' ', '') for link in
                                     browser.find_elements_by_xpath('''//h3[contains(@class, 'olpSellerName')]//a''')]))
            seller_names.sort()

            print 'asin: {}, seller:[{}]'.format(asin, seller_names)

            if included or len(filter(lambda seller: seller.upper() not in our_seller, seller_names)) > 0:
                thieves.append({'asin': asin, 'site': site, 'seller': ', '.join(seller_names), 'url': url})
                logger.info(
                    'find chief: {}, site: {}, seller: [{}], url: {}'.format(asin, site, ', '.join(seller_names), url))

    browser.quit()

    return thieves
