
from selenium import webdriver
from time import sleep

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chaojiying
import requests
from lxml import etree
from selenium.webdriver import ChromeOptions

#实现无可视化界面的操作
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#如何实现让selenium规避被检测到的风险
option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])

#登录页面
def login(username,password):
    s = Service(executable_path='./chromedriver.exe')
    bro = webdriver.Chrome(service=s,options=chrome_options)
    bro.get('http://jw.gzgs.edu.cn/eams/login.action')

    userName_tag = bro.find_element(by='id',value='username')
    password_tag = bro.find_element(by='id',value='password')
    userName_tag.send_keys(username)
    sleep(1)
    password_tag.send_keys(password)
    sleep(1)
    btn = bro.find_element(by='class name',value='blue-button')
    btn.click()
    sleep(1)
    return bro

#获取部分成绩
def get_score(bro):
    print('正在获取部分成绩列表')
    bro.get('http://jw.gzgs.edu.cn/eams/teach/grade/course/person.action')
    sleep(1)
    all_score = bro.find_element(by='class name', value='toolbar-item-ge0')
    all_score.click()
    sleep(1)
    score_data = bro.find_element(by='class name', value='gridtable')
    data_even = score_data.find_elements(by='class name', value='griddata-even')
    data_odd = score_data.find_elements(by='class name', value='griddata-odd')
    data = []
    score_list = []
    li = ['学年度','学期','门数','总学分','平均绩点']
    for even in data_even:
        even = even.text.split(' ')
        if len(even) != 5:
            continue
        data.append(even)
    for odd in data_odd:
        odd = odd.text.split(' ')
        if len(odd) != 5:
            continue
        data.append(odd)
    for d in data:
        score_list.append(dict(zip(li,d)))
    with open('./my_score.txt','w',encoding='utf-8') as fp:
        for score in score_list:
            fp.write(str(score))
            fp.write('\n')

#成绩列表
def get_score_list(bro):
    print('正在获取成绩列表')
    bro.get('http://jw.gzgs.edu.cn/eams/teach/grade/course/person.action')
    sleep(1)
    all_score = bro.find_element(by='class name', value='toolbar-item-ge0')
    all_score.click()
    sleep(1)
    score_data = bro.find_element(by='id',value='grid21344342991_data')
    data_even = score_data.find_elements(by='class name', value='griddata-even')
    data_odd = score_data.find_elements(by='class name', value='griddata-odd')
    data = []
    score_li = []
    li = ['学年','学期', '课程代码', '课程序号', '课程名称', '课程类别','学分','平时成绩','期中成绩','期末成绩','总评成绩','绩点']
    for even in data_even:
        even = even.text.split(' ')
        data.append(even)
    for odd in data_odd:
        odd = odd.text.split(' ')
        data.append(odd)
    for d in data:
        score_li.append(dict(zip(li, d)))
    with open('score_list.txt','w',encoding='utf-8') as fp:
        for score in score_li:
            fp.write(str(score))
            fp.write('\n')


if __name__ == '__main__':
    username = input('请输入学号：')
    password = input('请输入密码：')
    bro = login(username,password)
    get_score(bro)
    get_score_list(bro)