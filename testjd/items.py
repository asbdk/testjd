# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class TestjdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = "notebook"
    # 抓取数据对象
    sku = scrapy.Field()
    full_name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    shop = scrapy.Field()
    icons = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    graphics_card = scrapy.Field()
    cpu = scrapy.Field()
    thickness = scrapy.Field()
    memory = scrapy.Field()
    weight = scrapy.Field()
    disk = scrapy.Field()
    screen_size = scrapy.Field()
    good_rate = scrapy.Field()
    all_evaluation = scrapy.Field()
    top_evaluation = scrapy.Field()
    middle_evaluation = scrapy.Field()
    low_evaluation = scrapy.Field()
    detail = scrapy.Field()
    self_sell = scrapy.Field()
    pass
