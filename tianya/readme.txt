跑了3个页面就关闭爬虫，并且并发请求为1，开发的时候使用
scrapy crawl tianya -s CLOSESPIDER_PAGECOUNT=3 -s CONCURRENT_REQUEST=1

生成3个item就关闭爬虫，并发请求为1
scrapy crawl tianya -s CLOSESPIDER_ITEMCOUNT=3 -s CONCURRENT_REQUEST=1
