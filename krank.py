# -*- coding: utf-8 -*-
import logging
import logging.config

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def search(asin, site, words):
    logging.config.fileConfig('logging.conf', defaults={'type': 'rank'})
    logger = logging.getLogger('mylogger')

    logger.info('site: ' + site)
    logger.info('asin: ' + asin)
    logger.info('words:')
    for word in words:
        logger.info(word)

    results = []
    odwords = set()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:1080")
    browser = webdriver.Chrome('/home/mike/bin/chromedriver', chrome_options=chrome_options)
    browser.get(site)

    for word in words:
        if word.lower() not in odwords:
            try:
                browser.find_element_by_id('twotabsearchtextbox').clear()
                browser.find_element_by_id('twotabsearchtextbox').send_keys(unicode(word.decode("utf-8")))
                browser.find_element_by_name('site-search').submit()

                dl = 0
                cl = True
                for count in range(1, 21):

                    wait = WebDriverWait(browser, 10)
                    wait.until(expected_conditions.text_to_be_present_in_element((By.CLASS_NAME, "pagnCur"), str(count)))

                    browser.execute_script('''window.scrollTo(0, document.body.scrollHeight);''')

                    page = int(browser.find_element_by_class_name('pagnCur').get_attribute('innerHTML'))
                    logger.info('check: {}, current page: {}'.format(word, page))

                    # 遍历item
                    position = 1
                    for item_container in browser.find_elements_by_xpath(
                            "//div[@class='s-item-container'][.//a[contains(@class, 's-access-detail-page')]]"):
                        link = item_container.find_element_by_xpath(".//a[contains(@class, 's-access-detail-page')]")
                        href = link.get_attribute('href')

                        if asin in href:
                            try:
                                if len(item_container.find_element_by_xpath('.//h5').text) > 0:
                                    is_sponsored = True
                                else:
                                    is_sponsored = False
                            except:
                                is_sponsored = False
                            finally:
                                results.append({"word": word, "page": page, "position": position, "is_sponsored": is_sponsored})
                                logger.info(
                                    'check: {}, page: {}, position: {}, is_sponsored: {}'.format(word, page, position, is_sponsored))

                                dl += 1
                        else:
                            position += 1

                    # 遍历侧边栏
                    try:
                        if cl:
                            links = browser.find_elements_by_xpath(
                                "//div[contains(@class,'pa-ad-details')]/div[@class='a-section']/div[@class='a-section a-spacing-none pa-str-truncate']/a")

                            if len(links) == 0:
                                raise

                            for link in links:
                                href = link.get_attribute('href')
                                if asin in href:
                                    results.append({"word": word, "page": page, "position": 0, "is_sponsored": True})
                                    logger.info(
                                        'check: {}, page: {}, position: {}, is_sponsored: {}'.format(word, page, 0, True))
                                    cl = False
                                    break
                    except:
                        if page == 1:
                            cl = False

                    if dl == 2 and not cl:
                        break

                    # 下一页
                    try:
                        if page == 20:
                            continue

                        page_next = browser.find_element_by_class_name('pagnNext')
                        if len(page_next.get_attribute('href')) > 0:
                            page_next.click()
                        else:
                            break
                    except:
                        logger.info('word: {}, cur page: {}, except click'.format(word, page))
                        break
            except:
                logger.info('check except:' + word)
            finally:
                odwords.add(word.lower())

    logger.info('\n\ncheck word results:')
    for result in results:
        logger.info('{}, {}, {}, {}'.format(result['word'], result['page'], result['position'], result['is_sponsored']))

    browser.quit()

    return results
