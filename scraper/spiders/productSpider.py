from urllib.parse import urljoin

import scrapy
import json

class MySpider(scrapy.Spider):
    name = 'productSpider'
    allowed_domains = ['goldonecomputer.com']
    start_urls = ['https://www.goldonecomputer.com/']

    def _parse(self):
        url =  ['https://www.goldonecomputer.com/'];
        yield scrapy.Request(url, callback=self._parse())


    def parse(self, response):
        category_links = response.xpath("//*[@class='box-content']/ul[@id='nav-one']/li/a/@href").getall()

        for category_link in category_links:
            absolute_line = response.urljoin(category_link)
            yield scrapy.Request(absolute_line, callback=self.navigateLink)


    def navigateLink(self, response):
        product_links = response.xpath("//*[@class='caption']/h4/a/@href").getall()

        for product_link in product_links:
            absolute_line = response.urljoin(product_link)
            yield scrapy.Request(absolute_line, callback=self._parse())



    # def parse_category(self, response):
    #     # Step 2: Scrape product links within the category
    #     product_links = response.xpath("//*[@class='caption']/h4/a/@href").getall()
    #
    #     # Iterate through product links and follow each one
    #     for product_link in product_links:
    #         print(product_link)
            # yield response.follow(product_link, callback=self.parse_product)
