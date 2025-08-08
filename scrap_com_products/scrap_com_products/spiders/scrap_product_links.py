import scrapy
import json

class ScrapProductLinksSpider(scrapy.Spider):
    name = "scrap_product_links"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/"]

    def request_each_links(self):
        with open('categories_links.json', 'r') as f:
            urls = json.laod(f)
        for item in urls:
            yield scrapy.Request(url=item['url'], callback=self.parse)

    def parse(self, response):
        detail_links = response.xpath('//div[@id="content"]//div[contains(@class, "product-block product-thumb")]//a')

        for link in detail_links:
            product = link.css('::text').get()
            product_link = link.xpath('@href').get()

            if not product and product_link:
                print("Skipping the none product and product link...")
                continue
            
            yield {
                'product' : product,
                'link' : product_link
            }

