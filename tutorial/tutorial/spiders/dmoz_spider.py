import scrapy
import json
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["myapp.com"]
    start_urls = [
        "http://android.myapp.com/myapp/category.htm?orgame=1"
    ]

    def parse(self, response):
        for href in response.xpath('//li[contains(@id,"cate")]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_category)

    def generateSubRequest(self,response):
        categoryId = self.generateCategoryId(response.request)
        
        for index in [0,1,2,3,4]:
            url = "http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=%s&pageSize=20&pageContext=%d" % (categoryId,40 + index*20)
            print(url)
            yield scrapy.Request(url, callback=self.parse_json)
        
    def parse_json(self,response):
        apps = json.loads(response.body)
        for app in apps["obj"]:
            item = DmozItem()
            item['title'] = app["appName"]
            item['pkg'] = app["pkgName"]
            item["link"] = app["iconUrl"]
            yield scrapy.Request(app["iconUrl"], callback=self.download_image,meta={'pkg':item['pkg']})
            yield item
        #generate image request
        
    def download_image(self,response):
        pkg = response.request.meta['pkg']
        file=open("/tmp/images/%s.png" % pkg, "wb")
        file.write(response.body)
        file.flush()
        file.close()
    
    def generateCategoryId(self,request):
        url = request.url
        idx = url.index("categoryId=") + 11
        categoryId = url[idx:]
        return categoryId
        
    def parse_category(self, response):
        
        for request in self.generateSubRequest(response):
            yield request 
        
        for sel in response.xpath('//div[contains(@class,"app-info")]'):
            item = DmozItem()
            item['title'] = sel.xpath('(div/a[contains(@class,"name")]/text())[1]').extract()
            detailUrl = sel.xpath('div/a[contains(@class,"name")]/@href').extract()
            if(len(detailUrl) > 0):
                detail = detailUrl[0]
                if detail != None and detail.strip() != '':
                    ss = detail.index("=")
                    pkg = detail[ss + 1:]
                    item['pkg'] = pkg
            
            item['link'] = sel.xpath('a[contains(@class,"app-info-icon")]/img/@data-original').extract()
            if(len(item['link']) > 0):
                yield scrapy.Request(item["link"][0], callback=self.download_image,meta={'pkg':item['pkg']})
            yield item
            
    