#coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from tianya.utils.utils import *
import time

class TianyaPipeline(object):
    
    folder = "/data/crawler/tianya"
    mongoUtils = MongoUtils()
    
    def process_item(self, item, spider):
#         output = codecs.open(self.folder + '/' +item['title'], "w", "utf-8")
#         output = open(self.folder + '/' +item['title'], 'w')
#         print item['title']
        entry = {}
        entry['url'] = item['url']
        entry['title'] = item['title']
        entry['content'] = ""
        entry['insert_time'] = time.time()
        for content in item['content']:
            if(content != None):
                entry['content'] += "    " + content.strip() + "\n"
#             output.write(content)
        self.mongoUtils.insert(entry)
#         print item['title']
#         return item
        