#coding=utf-8

import scrapy
import json
from tianya.items import TianyaItem
from tianya.utils.commonUtils import *
from scrapy.utils.response import get_base_url
from w3lib.url import urljoin_rfc

class DmozSpider(scrapy.Spider):
    name = "tianya"
    allowed_domains = ["tianya.cn"]
    start_urls = [
        "http://bbs.tianya.cn"
    ]

    def parse(self, response):
        baseUrl = get_base_url(response)
        xxx = response.xpath('//a/@href').extract()
        for singleUrl in xxx:
            if(not regexMatch(singleUrl, ".*\.shtml$")):
                continue
            
            if(regexMatch(singleUrl, "^/.*\.shtml$")):
                #处理相对路径
                singleUrl = urljoin_rfc( baseUrl,singleUrl)
            
            if(singleUrl.find("bbs.tianya.cn") == -1):
                continue
                
            if(singleUrl.find('post-') != -1):
                yield scrapy.Request(singleUrl, callback=self.parse_post)
            else:
                yield scrapy.Request(singleUrl, callback=self.parse)
            
    def parse_post(self,response):
        titles = response.xpath('//span[contains(@class,"s_title")]/span/text()').extract()
        if(titles ==None or len(titles) == 0):
            return
        
        title = titles[0]
        item = TianyaItem()
        item['title'] = title
        item['content'] = []
        item['url'] = response.request.url
        for content in response.xpath('//div[contains(@class,"bbs-content")]/text()'):
            text = content.extract()
            item['content'] .append(text.strip())
        yield item
            
            