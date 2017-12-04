#!/usr/bin/python
# -*- coding: <encoding name> -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox(executable_path='./geckodriver')

browser.get('http://www.bing.com/')

elem = browser.find_element_by_id('sb_form_q')
elem.send_keys('bndy.net' + Keys.RETURN)

WebDriverWait(browser, 10).until(EC.title_is(u'bndy.net - Bing'))
browser.save_screenshot('~bndy-net.png')

browser.quit()
