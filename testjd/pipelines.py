# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from testjd.items import TestjdItem
import pymongo
class TestjdPipeline(object):
    def process_item(self, item, spider):
        return item

# 数据清洗
class AnalysisDataClearPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,TestjdItem):
            for detail in item['detail']:
                infos = detail.split("：")
                if infos[0] == "商品名称":
                    item['name'] = infos[1]
                elif infos[0] == "商品毛重":
                    item['weight'] = infos[1]
                elif infos[0] == "屏幕尺寸":
                    item['screen_size'] = infos[1]
                elif infos[0] == "内存容量":
                    item['memory'] = infos[1]
                elif infos[0] == "显卡型号":
                    item['graphics_card'] = infos[1]
                elif infos[0] == "处理器":
                    item['cpu'] = infos[1]
                elif infos[0] == "硬盘容量":
                    item['disk'] = infos[1]
                elif infos[0] == "厚度":
                    item['thickness'] = infos[1]
            # if "自营" in item['icons']:
            #     item['self_sell'] = True
            # else:
            #     item['self_sell'] = False
        return item

class MongoPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
    def close_spider(self,spider):
        self.client.close()
    def process_item(self, item, spider):
        new_item = dict(item)
        del new_item['detail']
        self.db[item.collection].update({
            'sku':item.get('sku')
        },{'$set':new_item},True)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get("MONGO_URL"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )