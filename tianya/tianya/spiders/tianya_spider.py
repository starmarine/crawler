#coding=utf-8

import scrapy
import json
from tianya.items import TianyaItem

class DmozSpider(scrapy.Spider):
    name = "tianya"
    allowed_domains = ["tianya.cn"]
    start_urls = [
        "http://focus.tianya.cn"
    ]

    def parse(self, response):
        for href in response.xpath('//h3/a[contains(@href,"post-")]'):
            title = href.xpath('@title').extract()
            url = href.xpath('@href').extract()
#             print title[0]
#             print url[0]
            yield scrapy.Request(url[0],meta={'title':title[0]}, callback=self.parse_single_page)

    def parse_single_page(self,response):
#         print(response.request)
#         print '殴事件'
        title = response.meta['title']
        item = TianyaItem()
        item['title'] = title
        item['content'] = []
        item['url'] = response.request.url
        for content in response.xpath('//div[contains(@class,"bbs-content")]/text()'):
            text = content.extract()
            item['content'] .append(text.strip())
        yield item
            
            