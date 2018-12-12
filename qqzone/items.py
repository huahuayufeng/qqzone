# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqzoneItem(scrapy.Item):
    # define the fields for your item here like:
    t_id=scrapy.Field()
    name = scrapy.Field()
    createtime = scrapy.Field()
    content=scrapy.Field()
    source_name=scrapy.Field()
    commentqq_id=scrapy.Field()
    commentName = scrapy.Field()
    commentContent = scrapy.Field()
    commentTime=scrapy.Field()
    picurl=scrapy.Field()
    piclocalAdd=scrapy.Field()

class PicItem(scrapy.Item):
    # define the fields for your item here like:
    msg_id = scrapy.Field()
    pic_num=scrapy.Field()
    url=scrapy.Field()

