# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
import json
import time

def get_cookies():
    browser = webdriver.Firefox()
    browser.get("https://user.qzone.qq.com/1033780738/infocenter")# xxx 改为qq账号
    cookie={}
    for i in browser.get_cookies():
        cookie[i["name"]] = i["value"]
    with open("D:\cookies.txt","w") as f:
        f.write(json.dumps(cookie))
    # time.sleep(5)
    # button = browser.find_element_by_xpath('//*[@id="switcher_plogin"]')
    # button.click()

    #browser.close()
"""
def get_content():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    with open("D:\cookies.txt","r")as f:
        cookies = f.read()
        cookies = json.loads(cookies)
    session = requests.session()
    html = session.get("https://user.qzone.qq.com/1033780738/infocenter",headers={"User-Agent":user_agent},cookies=cookies) # xxx改为qq账号
    print html.text
"""
def getGTK(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)
    return hashes & 0x7fffffff

if __name__ == "__main__":
    #get_cookies()
    #get_content()
    a=getGTK('@Qrh2a6FHo')
    print a