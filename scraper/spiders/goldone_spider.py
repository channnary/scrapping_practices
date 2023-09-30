import json

import scrapy
from urllib.parse import urljoin

class GoldOneSpider(scrapy.Spider):
    name = "goldone"
    start_urls = ['https://www.goldonecomputer.com/']

    def parse(self, response):
        # Step 1: Scrape all the categories' links
        # category_links = response.xpath('//div[@id="menu"]/ul/li/a/@href').extract()
        category_links = response.xpath("//*[@class='box-content']/ul[@id='nav-one']/li/a/@href").extract()
        for category_link in category_links:
            category = response.follow(category_link, callback=self.parse_category)
            # category = {
            #     'category': response.xpath('//*[@id="nav-one"]/li/a/text()').get()
            # }
            yield category

    def parse_category(self, response):
        # Step 2: Follow each category link and scrape product links
        product_links = response.xpath("//*[@class='caption']/h4/a/@href").extract()
        for product_link in product_links:
            product_url = urljoin(response.url, product_link)
            product = response.follow(product_url, callback=self.parse_product)
            yield product
            # print(product_url);

    def parse_product(self, response):
        # Step 3: Scrape product details
        product_detail = {
            'code': response.xpath('//*[@id="content"]/div[1]/div[2]/ul[1]/li[2]/text()').get(),
            'title': response.xpath('//*[@id="content"]/div[1]/div[2]/h3/text()').get(),
            'brand': response.xpath('//*[@id="content"]/div[1]/div[2]/ul[1]/li[1]/a/text()').get(),
            'price': response.xpath('//ul[@class="list-unstyled price"]/li/h3/text()').get(),
            'review_count': response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/a[1]/text()').get(),
            'image': response.xpath('//*[@id="tmzoom"]/@src').get(),
        }
        # with open('goldone_products.json', 'a', encoding='utf-8') as f:
        #     json.dump(product_detail, f, ensure_ascii=False, indent=4)
        #     f.write('\n')

        yield product_detail
