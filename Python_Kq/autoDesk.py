#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import datetime
import numpy
import os
import random
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

def get_imgs(driver):
    driver.save_screenshot('imgs/screenshot.png')
    bigImage = driver.find_element_by_id('bigImage')
    left = (int)(bigImage.location['x'])
    top = (int)(bigImage.location['y'])
    elementWidth = (int)(bigImage.location['x'] + bigImage.size['width'])
    elementHeight = (int)(bigImage.location['y'] + bigImage.size['height'])
    picture = Image.open('imgs/screenshot.png')
    picture = picture.crop((left, top, elementWidth, elementHeight))
    picture.save('imgs/big_full.png')
    smallImage = driver.find_element_by_id('smallImage')
    left = (int)(smallImage.location['x'])
    top = (int)(smallImage.location['y'])
    elementWidth = (int)(smallImage.location['x'] + smallImage.size['width'])
    elementHeight = (int)(smallImage.location['y'] + smallImage.size['height'])
    picture = Image.open('imgs/screenshot.png')
    picture = picture.crop((left, top, elementWidth, elementHeight))
    picture.save('imgs/small.png')
    jigimgS = driver.find_element_by_class_name('jigimgS')
    upper = (int)(jigimgS.value_of_css_property("top").split('px')[0])
    letf = 58
    right = 279
    lower = upper + 57
    picture = Image.open('imgs/big_full.png')
    picture = picture.crop((letf, upper, right, lower))
    picture.save('imgs/big.png')
    time.sleep(0.5)

def get_distance():
    target = cv2.imread("imgs/big.png")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('imgs/target.png', target)
    template = cv2.imread("imgs/small.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    width, height = template.shape[::-1]
    cv2.imwrite('imgs/template.png', template)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = numpy.unravel_index(result.argmax(), result.shape)
    y += 57
    time.sleep(0.5)
    return y

def move_mouse(driver, distance):
    time.sleep(0.5)
    has_gone_dist = 0
    remaining_dist = distance
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        if ratio < 0.1:
            span = random.randint(3, 5)
        elif ratio > 0.9:
            span = random.randint(5, 8)
        else:
            span = random.randint(15, 20)
        ActionChains(driver).move_by_offset(span, random.randint(-5, 5)).perform()
        remaining_dist -= span
        has_gone_dist += span
        time.sleep(random.randint(5, 20) / 100)

    ActionChains(driver).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
    ActionChains(driver).release().perform()

def main():
    chrome_options = webdriver.ChromeOptions()
   #chrome_options.add_argument('headless')
   #chrome_options.add_argument('no-sandbox')
   #chrome_options.add_argument('--disable-driver-side-navigation')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # Debug用
    driver.get("http://kq.neusoft.com/")
    with open('page1.html', 'w',encoding="UTF-8") as f:  
        f.write(driver.page_source)
    time.sleep(0.5)
    os.system('/bin/mkdir imgs')

    verify_text = driver.find_element_by_class_name("ui-slider-text")
    success = "验证成功"
    counter = 5
    while True:
        if counter < 1:
            driver.close()
            driver.quit()
            os.system('/bin/rm -fr imgs')
            exit()
        verify_btn = driver.find_element_by_class_name("ui-slider-btn")
        ActionChains(driver).move_to_element(verify_btn).perform()
        ActionChains(driver).click_and_hold(verify_btn).perform()
        time.sleep(0.5)
        get_imgs(driver)
        distance = get_distance()
        move_mouse(driver, distance + 20)
        time.sleep(0.5)
        counter -= 1
        if success in verify_text.text:
            break

    driver.find_element_by_class_name("userName").send_keys("tengyb")
    driver.find_element_by_class_name("password").send_keys("18345093167ASdgy123")

    driver.find_element_by_id("loginButton").click()
    with open('page2.html', 'w') as f:
        f.write(driver.page_source)
    time.sleep(0.5)
    driver.find_element_by_xpath('//a[@href="'+"javascript:document.attendanceForm.submit();"+'"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//a[@href="'+"javascript:exitAttendance();"+'"]').click()
    driver.close()
    driver.quit()
    os.system('/bin/rm -fr imgs')
    exit()

if __name__ == "__main__":
    main()
