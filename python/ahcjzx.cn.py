#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# TODO: fill username and password for logging in site
user = ''
password = ''

# Maybe you need to set permission for drivers
isWindows = platform.system() == 'Windows'
driverPath = './geckodriver.exe' if isWindows else './geckodriver'
browser = webdriver.Firefox(executable_path=driverPath)
browser.get('http://www.ahcjzx.cn/portal/')

elemName = browser.find_element_by_name('userKey')
elemPwd = browser.find_element_by_name('pwd')
elemName.send_keys(user)
elemPwd.send_keys(password)

browser.find_element_by_id('login_submit').click();
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'loginAfter')))
browser.get('http://www.ahcjzx.cn/studentstudio')
WebDriverWait(browser, 10).until(EC.title_is(u'未结束课程 - 安徽继续教育在线'))
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'lesson')))

baseWindow = browser.current_window_handle
videoLessons = []

courses = browser.find_elements_by_class_name('lesson')
for course in courses:
    des = course.find_elements_by_class_name('lesson-schedule')
    if len(des) > 0 and des[0].get_attribute('title').find('100%') > 0:
        # skip completed courses
        continue

    print('============ ' + des[0].get_attribute('title') + ' ===========')

    # go to sourse detail page
    courseName = course.find_element_by_class_name('lesson-name').get_attribute('title')
    link = course.find_element_by_class_name('lesson-view');
    link.click()
    WebDriverWait(browser, 10).until(EC.new_window_is_opened((browser.window_handles)))
    browser.switch_to_window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sh-res')))

    # get all lessions
    lessons = browser.find_elements_by_class_name('sh-res')
    for lesson in lessons:
        if len(lesson.find_elements_by_class_name('video')) > 0:
            # only video lessons
            if len(lesson.find_elements_by_class_name('icon-iconfontyuan')) > 0:
                # skip completed items
                continue

            # get link urls
            link = lesson.find_element_by_tag_name('a')
            lessonName = link.get_attribute('title')
            videoLessons.append([courseName, lessonName, link.get_attribute('href')])
            print(lessonName)
    browser.close()
    browser.switch_to_window(baseWindow)

print('--------- Unfinished Lessons ---------') 
for lesson in videoLessons:
    print(datetime.now() + '    ' + lesson[0] + ' > ' + lesson[1] + ' ...')
    browser.get(lesson[2])
    WebDriverWait(browser, 60 * 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-green')))
    print(datetime.now() + '    Done')
        
#browser.quit()
