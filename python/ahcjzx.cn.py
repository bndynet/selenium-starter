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

isWindows = platform.system() == 'Windows'
driverPath = '../drivers/geckodriver.exe' if isWindows else '../drivers/geckodriver'
browser = webdriver.Firefox(executable_path=driverPath)
baseWindow = browser.current_window_handle

def print_msg(msg):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S %p') + '    ' + msg)

def print_done():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S %p') + '    ' + '完成')

def login():
    print_msg('开始站点登录...')
    browser.get('http://www.ahcjzx.cn/portal/')

    elemName = browser.find_element_by_name('userKey')
    elemPwd = browser.find_element_by_name('pwd')
    elemName.send_keys(user)
    elemPwd.send_keys(password)

    browser.find_element_by_id('login_submit').click()
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'loginAfter')))
    print_done()

def get_courses():
    print_msg('正在获取课程信息...')
    courses = []
    browser.get('http://www.ahcjzx.cn/studentstudio')
    WebDriverWait(browser, 10).until(EC.title_is(u'未结束课程 - 安徽继续教育在线'))
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'lesson')))
    eleCourses = browser.find_elements_by_class_name('lesson')
    for eleCourse in eleCourses:
        des = eleCourse.find_elements_by_class_name('lesson-schedule')
        courseName = eleCourse.find_element_by_class_name('lesson-name').get_attribute('title')
        courseTitle = des[0].get_attribute('title')
        courseUrl = eleCourse.find_element_by_class_name('lesson-view').get_attribute('data-href')
        courseIsDone = False

        if len(des) > 0 and des[0].get_attribute('title').find('100%') > 0:
            courseIsDone = True
            continue

        courses.append((courseTitle, courseName, courseIsDone, courseUrl))
    return courses


def get_course_lessions(course):
    print_msg(course[0] + '...')
    rootUrl ='http://www.ahcjzx.cn/' + course[3]
    videoLessons = []
    browser.get(rootUrl)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sh-res')))

    print('============ 剩余视频课程 ===========') 
    lessons = browser.find_elements_by_class_name('sh-res')
    for lesson in lessons:
        if len(lesson.find_elements_by_class_name('video')) > 0:
            link = lesson.find_element_by_tag_name('a')
            lessonName = link.get_attribute('title')
            lessonUrl = link.get_attribute('href')
            lessonIsDone = False
            # in-process: iconfont recent-icon
            # not started: iconfont icon-yuan
            # completed: iconfont icon-iconfontyuan
            if len(lesson.find_elements_by_class_name('icon-iconfontyuan')) > 0:
                lessonIsDone = True
            else:
                print('    ' + lessonName)
            videoLessons.append((lessonName, lessonUrl, lessonIsDone))

    return videoLessons

def start_learning(course):
    for lesson in course[4]:
        if lesson[2]:
            continue
        print_msg(course[1] + ' - ' + lesson[0] + '...')
        browser.get(lesson[1])
        WebDriverWait(browser, 60 * 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-green')))
        print_done()
        
login()
courses = get_courses()
finalCourses = []
for course in courses:
   finalCourses.append(course + (get_course_lessions(course),))

for course in finalCourses:
    print('')
    print('============ 开始视频学习 ===========') 
    if not course[2]:
        start_learning(course)

browser.close()
