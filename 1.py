# coding:utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium import webdriver
from aip import AipOcr
from PIL import Image
import time
import os


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 60, 0.01)
url = "http://kgy.jiashiren.vip/login.aspx#"


def login_web():
    browser.set_window_size(1024, 768)
    browser.get(url)
    wait.until(EC.visibility_of_element_located((By.ID, 'stuid')))
    code_img_get()
    img_trans()
    load_userdata()


def load_userdata():
    browser.find_element_by_id('stuid').clear()
    browser.find_element_by_id("psw").clear()
    browser.find_element_by_id("code").clear()
    browser.find_element_by_id('stuid').send_keys('流水号')
    browser.find_element_by_id("psw").send_keys('密码'')
    code = code_client()
    browser.find_element_by_id("code").send_keys(code)
    time.sleep(0.3)
    browser.find_element_by_xpath('//*[@id="ImageButton1"]').click()
    time.sleep(0.3)
    result = EC.alert_is_present()(browser)
    if result:
        time.sleep(0.2)
        browser._switch_to.alert.accept()
        time.sleep(0.2)
        code_img_get()
        img_trans()
        load_userdata()
    else:
        login_timewait()


def login_timewait():
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="form1"]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[1]/a[1]')))
    browser.find_element_by_xpath(
        '//*[@id="form1"]/table[2]/tbody/tr/td[2]/table/tbody/tr/td[1]/a[1]').click()
    time.sleep(0.2)
    result = EC.alert_is_present()(browser)
    if result:
        time.sleep(0.1)
        browser._switch_to.alert.accept()
        time.sleep(0.1)
        login_timewait()
    else:
        login_crouse()


def login_crouse():
    browser.get(
        'http://kgy.jiashiren.vip/book1bycoach.aspx?traintype=%u79d1%u76ee%u4e8c&coachname=%u9b4f%u7d20%u971e')

    wait.until(EC.visibility_of_element_located((By.ID, '0')))
    number_all = len(browser.find_elements_by_tag_name('a'))
    number_choice = len(
        browser.find_elements_by_partial_link_text('约车'))
    if number_choice > 6:
        x = range(number_all-11, number_all-8)
    else:
        x = range(number_all - 3, number_all)
    for ix in x:
        a = '//*[@ id="'+str(ix)+'"]'
        browser.find_element_by_xpath(a).click()
        b = 1
        while b < 4:
            try:
                print('尝试')
                WebDriverWait(browser, 0.3, 0.05).until(
                    EC.alert_is_present())
                browser._switch_to.alert.accept()
            except Exception:
                b += 1
        print(str(ix)+'可能已被他人选择，正在选择下一节课')
    print('选课结束')
    os.remove('code1.png')


def code_img_get():
    browser.save_screenshot('code1.png')
    element = browser.find_element_by_xpath(
        r'//*[@id="form1"]/table[4]/tbody/tr/td[2]/table/tbody/tr/td[2]/table[3]/tbody/tr/td[3]/img')
    left = element.location['x']
    top = element.location['y']
    right = left + element.size['width']
    bottom = top + element.size['height']
    img = Image.open('code1.png')
    imgcod = img.crop((left, top, right, bottom))
    imgcod.save('code1.png')


def code_client():
    APP_ID = '百度智能云'

    API_KEY = ''

    SECRET_KEY = ''

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    with open('code1.png', 'rb') as f:

        image = f.read()

        code1 = client.basicAccurate(image)
        code1 = code1['words_result'][0]['words']
        return(code1)


def img_trans():
    img = Image.open('code1.png')
    Img = img.convert('L')
    Img.save('code1.png')
    table = []
    for i in range(256):
        if i < 190:
            table.append(0)
        else:
            table.append(1)
    photo = Img.point(table, '1')
    photo.save('code1.png')


def img_size():
    im = Image.open('code1.png')
    (x, y) = im.size
    im = im.resize((x*100, y*100), Image.ANTIALIAS)
    im.save('code1.png')


if __name__ == '__main__':
    login_web()
