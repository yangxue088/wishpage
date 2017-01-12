# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import logging.config
import time

import os
from selenium import webdriver


def check_product_inventory(sites, asins):
    logging.config.fileConfig('logging.conf', defaults={'type': 'inventory'})
    logger = logging.getLogger('mylogger')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1080")
    browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)

    results = []
    ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for site in sites:
        for asin in asins:
            try:
                url = 'https://{}/dp/{}'.format(site, asin)
                browser.get(url)
                logger.info('current url: ' + url)

                merchant = '-'
                try:
                    merchants = browser.find_elements_by_xpath('''//*[@id='merchant-info']/a''')
                    if len(merchants) != 2:
                        logger.error('product is not FBA')
                        continue
                    else:
                        merchant = merchants[0].text
                except:
                    pass
                logger.info('merchant: ' + merchant)

                rank = ''
                try:
                    rank = browser.find_element_by_xpath('''//div[@id='prodDetails']//a[contains(@href,'bestsellers')]/ancestor::td''').text
                except:
                    try:
                        rank = browser.find_element_by_xpath(
                            '''//div[contains(@id, 'detail')]//a[contains(@href,'bestsellers')]/ancestor::li''').text
                    except:
                        pass
                finally:
                    if len(rank) == 0:
                        rank = '-'
                logger.info('rank: ' + rank)

                browser.find_element_by_id('add-to-cart-button').click()

                for x in range(1, 10):
                    try:
                        browser.get('https://{}/gp/cart/view.html'.format(site))
                        browser.find_element_by_xpath('''//span[@data-action="a-dropdown-button"]''').click()
                        browser.find_element_by_xpath('''//a[text()='10+']''').click()
                        browser.find_element_by_name('quantityBox').clear()
                        browser.find_element_by_name('quantityBox').send_keys('999')
                        browser.find_element_by_xpath('''//a[@data-action="update"]''').click()
                        suc = True

                        break
                    except:
                        time.sleep(2)
                        if x == 3:
                            suc = False
                            break

                if not suc:
                    logger.error('product inventory can not check')
                    continue

                price = browser.find_element_by_class_name('sc-product-price').text
                logger.info('price: ' + price)

                while True:
                    try:
                        inventory = browser.find_element_by_class_name('quantity').text
                    except:
                        inventory = browser.find_element_by_name('quantityBox').get_attribute('value')
                    finally:
                        try:
                            message = browser.find_element_by_class_name('sc-quantity-update-message').text
                            if len(inventory) > 0:
                                break
                        except:
                            time.sleep(1)

                logger.info('inventory: ' + inventory)
                logger.info('message: ' + message)
                results.append(
                    {'time': ctime, 'site': site, 'asin': asin, 'url': url, 'merchant': merchant, 'price': price, 'inventory': inventory,
                     'message': message,
                     'rank': rank})

                while True:
                    try:
                        for delete_item in browser.find_elements_by_class_name('sc-action-delete'):
                            delete_item.click()

                        if len(browser.find_elements_by_class_name('sc-action-delete')) == 0:
                            break
                        else:
                            browser.refresh()
                    except:
                        time.sleep(1)

            except:
                results.append(
                    {'time': ctime, 'site': site, 'asin': asin, 'url': url, 'merchant': merchant, 'price': price, 'inventory': 0,
                     'message': '-', 'rank': rank})
                logger.info('product can not check inventory, url: ' + url)

    browser.quit()

    # 生成报表
    filename = 'output/inventory.csv'
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(filename, 'ab+') as file:
        writer = csv.writer(file)

        if len(file.readlines()) == 0:
            writer.writerow(['时间', '站点', 'ASIN', '链接', '卖家', '价格', '库存', '排名', '提示'])

        for result in results:
            writer.writerow(
                [result['time'], result['site'], result['asin'], result['url'], result['merchant'], result['price'], result['inventory'],
                 result['rank'], result['message']])

    logger.info('generate inventory report finish, site: {}, asins: {}'.format(site, ', '.join(asins)))
    return results
