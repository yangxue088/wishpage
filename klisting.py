# -*- coding: utf-8 -*-
import datetime
import logging
import logging.config

from selenium import webdriver


def get_listing_info(sites, asins, child):
    logging.config.fileConfig('logging.conf', defaults={'type': 'listing'})
    logger = logging.getLogger('mylogger')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1080")
    browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)

    results = []

    for site in sites:

        index = 0
        while index < len(asins):
            asin = asins[index]
            index += 1

            ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                url = 'https://{}/dp/{}'.format(site, asin)
                browser.get(url)
                logger.info('current url: ' + url)

                # 扩展到其他子ASIN
                if child:
                    try:
                        child_asins = [elem.get_attribute('data-defaultasin') for elem in
                                       browser.find_elements_by_xpath('''//*[@data-defaultasin]''')]
                        extend_asins = [child_asin for child_asin in child_asins if child_asin not in asins]

                        if len(extend_asins) > 0:
                            asins.extend(extend_asins)
                            logger.info('extend asin from: {}, extend: {}'.format(asin, extend_asins))
                    except:
                        pass

                merchant = '-'
                try:
                    merchants = browser.find_elements_by_xpath('''//*[@id='merchant-info']//a''')
                    merchant = merchants[0].text
                except:
                    pass
                logger.info('merchant: ' + merchant)

                review_count = '-'
                try:
                    review_count_text = browser.find_element_by_id('acrCustomerReviewText').text
                    review_count = review_count_text[:review_count_text.index(' ')]
                except:
                    pass
                logger.info('review count: ' + review_count)

                review_rate = '-'
                try:
                    review_rate_text = browser.find_element_by_id('acrPopover').get_attribute('title')
                    review_rate = review_rate_text[:review_rate_text.index(' ')]
                except:
                    pass
                logger.info('review rate: ' + review_rate)

                price = '-'
                try:
                    price = browser.find_element_by_id('priceblock_saleprice').text
                except:
                    try:
                        price = browser.find_element_by_id('priceblock_ourprice').text
                    except:
                        pass
                logger.info('price: ' + price)

                title = '-'
                try:
                    title = browser.find_element_by_id('productTitle').text
                except:
                    pass
                logger.info('title: ' + title)

                rank = '-'
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

                results.append(
                    {'time': ctime, 'site': site, 'asin': asin, 'url': url, 'merchant': merchant, 'review_count': review_count,
                     'review_rate': review_rate,
                     'price': price, 'title': title,
                     'rank': rank})
            except:
                results.append(
                    {'time': ctime, 'site': site, 'asin': asin, 'url': url, 'merchant': '-', 'review_count': '-',
                     'review_rate': '-',
                     'price': '-', 'title': '-',
                     'rank': '-'})
                logger.info('product can not get listing info, url: ' + url)

    browser.quit()

    logger.info('get listing info finish!')
    return results
