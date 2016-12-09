# -*- coding: utf-8 -*-
import logging
import logging.config
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class KMatch(object):
    def __init__(self):
        pass

    def match(self, id, site, asins, words):

        logging.config.fileConfig('logging.conf', defaults={'type': 'relevance'})
        logger = logging.getLogger('mylogger')

        logger.info('site: ' + site)

        logger.info('words: ')
        for word in words:
            logger.info(word)

        logger.info('asins: ')
        for asn in asins:
            logger.info(asn)

        odwords = set()
        results = []
        excepts = []
        asin_map = {}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1080")
        browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)
        browser.get(site)

        for word in words:
            word = word.replace(u"\xc2\xa0", ' ').replace(u"\xa3\xa0", ' ').strip()
            if word.startswith(','):
                word = word[1:]
            elif word.endswith(','):
                word = word[:-1]

            if word.lower() not in odwords:
                try:
                    browser.find_element_by_id('twotabsearchtextbox').clear()
                    browser.find_element_by_id('twotabsearchtextbox').send_keys(unicode(word.decode("utf-8")))
                    browser.find_element_by_name('site-search').submit()

                    time.sleep(1)

                    wait = WebDriverWait(browser, 10)
                    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='s-item-container']")))

                    browser.execute_script('''window.scrollTo(0, document.body.scrollHeight);''')

                    # 获取亚马逊的单词纠错结果
                    try:
                        browser.find_element_by_xpath("//span[@id='didYouMean']/a[2]")
                        correct = browser.find_element_by_xpath("//span[@id='didYouMean']/a[1]").text

                        words.append(correct)
                        logger.info('correct from: {}, to: {}'.format(word, correct))

                        continue
                    except:
                        pass

                    # 在用长单词搜索的情况下，亚马逊会有短词推荐，获取亚马逊的推荐单词
                    try:
                        suggest_spans = browser.find_elements_by_xpath("//span[@class='a-size-base a-text-normal']")

                        if len(suggest_spans) > 0:
                            for suggest_span in suggest_spans:
                                suggest_word = ' '.join(
                                    [span.text for span in suggest_span.find_elements_by_xpath("span") if
                                     len(span.text) > 0 and span.text != "“" and span.text != "”"])

                                if len(suggest_word.strip()) == 0:
                                    words.append(word)
                                    logger.info('return to waiting list: ' + word)
                                    word = ''
                                    break

                                words.append(suggest_word)
                                logger.info('short from: {}, to: {}'.format(word, suggest_word))

                            continue
                    except:
                        logger.info('nothing long word: {}'.format(word))
                        pass

                    meet = 0
                    reviews = 0
                    brands = set()

                    for item_container in browser.find_elements_by_xpath(
                            "//div[@class='s-item-container'][.//a[contains(@class, 's-access-detail-page')]]"):

                        try:
                            link = item_container.find_element_by_xpath(".//a[contains(@class, 's-access-detail-page')]")
                            href = link.get_attribute('href')

                            for asn in asins:
                                if asn in href:
                                    if asn not in asin_map:
                                        try:
                                            summary_star = item_container.find_element_by_xpath(".//a[contains(@href, 'customerReviews')]")
                                            count = int(summary_star.text.strip())
                                            asin_map[asn] = count
                                        except:
                                            asin_map[asn] = 0
                                        finally:
                                            words.append(link.get_attribute('title'))
                                            logger.info('append from: {}, to: {}'.format(asn, link.get_attribute('title')))

                                    reviews += asin_map[asn]
                                    meet += 1

                                    brand = item_container.find_element_by_xpath(".//span[@class='a-size-small a-color-secondary'][2]")
                                    if len(brand.text) > 0:
                                        brands.add(brand.text)

                                    break
                        except:
                            pass

                    results.append((reviews, meet, word, brands))
                    logger.info('check: {}, match: {}, reviews: {}'.format(word, meet, reviews))
                except:
                    plogger.info('check except:' + word)
                    excepts.append(word)
                finally:
                    odwords.add(word.lower())

        browser.quit()

        logger.info('------------------------------------------')
        logger.info('hoho, except word as below:')
        logger.info('------------------------------------------')
        for word in excepts:
            logger.info(word)

        logger.info('------------------------------------------')
        logger.info('yeah, check word as below:')
        logger.info('------------------------------------------')
        results.sort(reverse=True)

        data = []

        for result in filter(lambda r: r[1] > 2 and len(r[3]) > 1 and len(r[2].split(' ')) < 8, results):
            if len(result[3]) > 0 and any(brand.lower() in result[2].lower() for brand in result[3] if len(brand) > 0):
                isbrand = True
                logger.info("{}| {}| {} -- {} -- *".format(result[0], result[1], result[2], ', '.join(result[3])))
            else:
                isbrand = False
                logger.info("{}| {}| {} -- {}".format(result[0], result[1], result[2], ', '.join(result[3])))

            data.append({"review": result[0], "meet": result[1], "word": result[2], "brand": ', '.join(result[3]), "isbrand": isbrand})

        return data
