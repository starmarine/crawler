# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

class TianyaPipeline(object):
    
    folder = "/tmp/tianya"
    
    def process_item(self, item, spider):
        output = codecs.open(self.folder + '/' +item['title'], "w", "utf-8")
#         output = open(self.folder + '/' +item['title'], 'w')
        print item['title']
        
        for content in item['content']:
            output.write(content)
#         print item['title']
        return item
