# -*- coding: utf-8 -*-
import scrapy
from testjd.items import TestjdItem
from urllib import parse
from scrapy.conf import settings
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672']

    def parse(self, response):
        items = response.css(".gl-item")
        for item in items:
            ItemObject = TestjdItem()
            ItemObject['sku'] = item.css(".gl-i-wrap.j-sku-item::attr(data-sku)").extract_first()
            ItemObject['full_name'] = item.css(".p-name>a>em::text").extract_first().strip()
            ItemObject['price'] = item.css(".p-price i::text").extract_first()
            ItemObject['shop'] = item.css(".p-shop a::attr(title)").extract_first()
            ItemObject['icons'] = ",".join(item.css(".p-icons>i::text").extract())
            ItemObject['stock'] = item.css(".p-stock::text").extract_first()
            url = item.css(".p-name>a::attr(href)").extract_first()
            url = parse.urljoin(response.url, url)
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': ItemObject, 'detail': 1})
        max_page = settings.get("MAX_PAGE", 0)
        next_url = response.css("a.pn-next::attr(href)").extract_first()
        curr_page = response.css("div.page a.curr::text").extract_first()
        if next_url:
            if curr_page is None or max_page == 0 or max_page > int(curr_page):
                yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        # 爬取详情页

    def parse_detail(self, response):
        item = response.meta['item']
        item['brand'] = response.css("#parameter-brand>li::attr(title)").extract_first()
        item['detail'] = response.css("ul.parameter2.p-parameter-list>li::text").extract()
        item['good_rate'] = response.css("div.percent-con::text").extract_first()
        item['all_evaluation'] = response.css(
            "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(1)::attr(data-num)").extract_first()
        item['top_evaluation'] = response.css(
            "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(5)::attr(data-num)").extract_first()
        item['middle_evaluation'] = response.css(
            "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(6)::attr(data-num)").extract_first()
        item['low_evaluation'] = response.css(
            "#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-child(7)::attr(data-num)").extract_first()

        return item
