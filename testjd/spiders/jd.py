# -*- coding: utf-8 -*-
import scrapy
from testjd.items import TestjdItem
from urllib import parse
from scrapy.conf import settings
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import json
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com','c0.3.cn']
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main']
    def parse(self, response):
        time.sleep(1)
        items = response.css(".gl-item")
        for item in items:
            ItemObject = TestjdItem()
            ItemObject['sku'] = item.css(".gl-i-wrap.j-sku-item::attr(data-sku)").extract_first()
            ItemObject['full_name'] = item.css(".p-name>a>em::text").extract_first().strip()

            ItemObject['icons'] = ",".join(item.css(".p-icons>i::text").extract())
            ItemObject['stock'] = item.css(".p-stock::text").extract_first()
            venderId = item.css(".gl-i-wrap.j-sku-item::attr(venderid)").extract_first()
            url = item.css(".p-name>a::attr(href)").extract_first()
            url = parse.urljoin(response.url, url)
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': ItemObject, 'detail': 1,'venderId':venderId})
        max_page = settings.get("MAX_PAGE", 0)
        next_url = response.css("a.pn-next::attr(href)").extract_first()
        curr_page = response.css("div.page a.curr::text").extract_first()
        if next_url:
            if curr_page is None or max_page == 0 or max_page > int(curr_page):
                yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        # 爬取详情页

    def parse_detail(self, response):
        time.sleep(1)
        item = response.meta['item']
        venderId = response.meta['venderId']
        item['brand'] = response.css("#parameter-brand>li::attr(title)").extract_first()
        item['detail'] = response.css("ul.parameter2.p-parameter-list>li::text").extract()

        url = 'https://c0.3.cn/stock?skuId='+item['sku']+'&area=22_1930_50947_0&venderId='+venderId+'&cat=670,671,672'
        yield scrapy.Request(url=url, callback=self.parse_price, meta={'item': item},encoding='utf-8')



        # item['good_rate'] = response.css("div.percent-con::text").extract_first()
        # item['all_evaluation'] = response.css(
        #     "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(1)::attr(data-num)").extract_first()
        # item['top_evaluation'] = response.css(
        #     "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(5)::attr(data-num)").extract_first()
        # item['middle_evaluation'] = response.css(
        #     "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(6)::attr(data-num)").extract_first()
        # item['low_evaluation'] = response.css(
        #     "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(7)::attr(data-num)").extract_first()

        return item

    def parse_price(self,response):
        item = response.meta['item']
        # t = response.body.decode('gbk')
        stock = json.loads(response.body.decode('gbk'))
        if stock['stock'].get('self_D'):
            item['shop'] = stock['stock']['self_D']['deliver']
            item['self_sell'] = True
        else:
            item['shop'] = stock['stock']['D']['deliver']
            item['self_sell'] = False

        item['price'] = stock['stock']['jdPrice']['p']
        item['stock'] = stock['stock']['StockStateName']
        url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + item['sku']
        yield scrapy.Request(url=url, callback=self.parse_comment, meta={'item': item})
        return item
    def parse_comment(self,response):
        item = response.meta['item']
        comments = json.loads(response.text)
        item['good_rate'] = comments['CommentsCount'][0]['GoodRate']
        item['all_evaluation'] = comments['CommentsCount'][0]['CommentCount']
        item['top_evaluation'] = comments['CommentsCount'][0]['GoodCount']
        item['middle_evaluation'] = comments['CommentsCount'][0]['GeneralCount']
        item['low_evaluation'] = comments['CommentsCount'][0]['PoorCount']
        return item

