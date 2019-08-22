# -*- coding: utf-8 -*-
import scrapy,time
from selenium import webdriver  # 调用这个模块
import json
import re
from ..items import QqzoneItem
from ..items import PicItem

class QqzoneSpider(scrapy.Spider):
    name = 'qqzone'
    allowed_domains = ['user.qzone.qq.com']
    qq_id=xxxxxxxxx
    friendqq_id=xxxxxxxxx
    gtk=0
    pos=-20
    g_qzonetoken = ''


    def start_requests(self):
        self.get_cookies()
        #friendurl='https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={0}&inCharset=utf-8&outCharset=utf-8&hostUin={0}&notice=0&sort=0&pos={3}&num=20&cgi_host=http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={1}&qzonetoken={2}'.format(
        #    str(self.friendqq_id), str(self.gtk), str(self.g_qzonetoken), str(self.pos))

        user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
        with open("D:\cookies.txt", "r") as f:
            cookies = f.read()
            cookies = json.loads(cookies) #获取cookies
        for i in range(100):
            self.pos+=20 #获取页码
            start_urls = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={0}&inCharset=utf-8&outCharset=utf-8&hostUin={0}&notice=0&sort=0&pos={3}&num=20&cgi_host=http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={1}&qzonetoken={2}'.format(
                str(self.qq_id), str(self.gtk), str(self.g_qzonetoken), str(self.pos))
            friendurl = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={0}&inCharset=utf-8&outCharset=utf-8&hostUin={0}&notice=0&sort=0&pos={3}&num=20&cgi_host=http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={1}&qzonetoken={2}'.format(
                str(self.friendqq_id), str(self.gtk), str(self.g_qzonetoken), str(self.pos))
            print(friendurl)
            yield scrapy.Request(friendurl,callback=self.parse,headers={'user-agent': user_agent},cookies=cookies)

    def parse(self, response):
        body=response.body.decode('utf-8')
        CallbackStr=re.search('_Callback\((.+)\)',body).group(1)
        jsonBody=json.loads(CallbackStr)
        print(jsonBody)
        #print data_body
        item=QqzoneItem()
        #picitem=PicItem()
        if('msglist' in jsonBody):
            if(jsonBody['msglist'] !=None):
                msglists=jsonBody['msglist']
                for msglist in msglists:
            #commentlists=msglist['commentlist']
            #for commentlist in commentlists:
             #   item['commentName']=commentlist['name']
             #   item['commentTime'] = commentlist['createTime2']
             #   item['commentContent'] = commentlist['content']
             #   item['commentqq_id'] = commentlist['uin']
                    if('tid' in msglist):
                        item['t_id']=msglist['tid']
                        #picitem['msg_id']=msglist['tid']
                    if ('name' in msglist):
                        item['name'] = msglist['name']
                    if ('content' in msglist):
                        item['content']=msglist['content']
                    if ('createTime' in msglist):
                        item['createtime'] = msglist['createTime']
                    if ('source_name' in msglist):
                        item['source_name'] = msglist['source_name']
                    # if('pic' in msglist):
                    #     pics = msglist['pic']
                    #     for pic in pics:
                    #         if ('pic_id' in msglist):
                    #             #picitem['url']=pic['pic_id'].replace('\\','')
                    #             #picitem['pic_num']=int(pic['absolute_position'])+1
                    yield item
        else:
            if ('tid' in jsonBody):
                item['t_id'] = jsonBody['tid']
            item['name']=jsonBody['name']
            item['content'] = jsonBody['msg']
            item['createtime'] = jsonBody['createTime']
            item['source_name'] = ''
            yield item



    def get_cookies(self):
        browser = webdriver.Firefox()
        browser.get("https://qzone.qq.com/")
        browser.switch_to.frame("login_frame")
        button = browser.find_element_by_css_selector('#switcher_plogin')
        button.click()
        account = browser.find_element_by_css_selector("#u")
        account.clear()
        account.send_keys("xxxxxxxx")  # 此处写账号
        password = browser.find_element_by_css_selector("#p")
        password.clear()
        password.send_keys("xxxxxxxx")  # 此处写密码

        login_button = browser.find_element_by_css_selector("#login_button")
        login_button.click()
        cookie = {}
        for i in browser.get_cookies():
            cookie[i["name"]] = i["value"]
        with open("D:\cookies.txt", "w") as f:
            f.write(json.dumps(cookie))
        time.sleep(5)
        browser.switch_to_default_content()
        html=browser.page_source
        #print html
        g_qzonetoken = re.search('window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)  # 从网页源码中提取g_qzonetoken
        #print g_qzonetoken
        self.g_qzonetoken = g_qzonetoken.group(1)
        self.gtk = self.getGTK(cookie)  # 通过getGTK函数计算gtk
        print(self.g_qzonetoken,self.gtk)


    def getGTK(self,cookie):
        hashes = 5381
        for letter in cookie['p_skey'] or cookie['skey'] or cookie['rv2'] or '':
            hashes += (hashes << 5) + ord(letter)
        return hashes & 0x7fffffff

   
