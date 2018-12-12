# -*- coding: utf-8 -*-
#导入selenium2中的webdriver库
import requests
import re

import time
import urllib3
from Queue import Queue
urllib3.disable_warnings()
session =requests.session()
user=input('输入登录的qq号:')
def cookielogin():
    global session
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
               'Referer': 'https://qzone.qq.com/',
               'Host': 'user.qzone.qq.com'}
    with open(r'D:\cookies.txt', 'r') as f:
        ans = f.readlines()

    for an in ans:
        an = an.replace('\n', '')
        a = an.split('==')
        cookies[a[0]] = a[1]
    cookies['_qz_referrer'] = 'i.qq.com'
    print(cookies)
    requests.utils.add_dict_to_cookiejar(session.cookies,cookies)
    r=session.get('https://user.qzone.qq.com/%s/infocenter'%(user),headers=headers,verify=False)
    if not re.findall('QQ空间-分享生活，留住感动',r.text):
        return  True
    else:
        return False

def login():
    from selenium import webdriver
    driver = webdriver.Firefox()
    driver.get('https://user.qzone.qq.com/')
    global session
    time.sleep(10)

    with open(r'D:\cookies.txt', 'w+') as f:
        for cookie in driver.get_cookies():
            f.write(cookie['name']+'=='+cookie['value']+'\n')
    f.close()
if __name__=="__main__":
    cookies={}
    q=Queue(maxsize=1000)

    url='https://user.qzone.qq.com/'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
             'Referer': 'https://qzone.qq.com/',
             'Host': 'user.qzone.qq.com'}
    if not cookielogin():
        login()
    r=session.get('https://user.qzone.qq.com/%s'%(user),headers=headers,verify=False)
    numble=re.findall('uin="(\d*?)"',r.text)
    for uin in numble:
        q.put(uin)
    while 1:
        if q.qsize()<=1000:
            r=session.get('https://h5.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds_html_act_all?uin=%s&hostuin=%s&start=10&count=60'%(user,q.get()),headers=headers,cookies=cookies,verify=False)
            ans=re.findall('(\d{8,10})',r.text,re.S)
            ans=set(ans)
            for an in ans :
                url='https://user.qzone.qq.com/%s'%(an)
                r=session.get(url,headers=headers,cookies=cookies,verify=False)
                if not len(re.findall('QQ空间-分享生活，留住感动',r.text,re.S)):

                    print(url)
                if q.qsize() <= 1000:
                    q.put(an)
                else:
                    break
        else:
            break





