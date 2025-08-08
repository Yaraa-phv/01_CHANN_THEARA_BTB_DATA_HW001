# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class ScrapComProductsPipeline:

    def __init__(self):
        self.all_product_data = {}

    def process_item(self, item, spider):
        spider.name = 'scrap_products'
        category = item.get('category', 'Unknown')
        product_data = item.get('product_data')
        if not category in self.all_product_data:
            self.all_product_data[category] = []

        self.all_product_data[category].append(product_data)
        return item

    def close_spider(self, spider):
        spider.name = 'scrap_products'
        with open('all_product.json', 'w', encoding = 'utf-8') as file:
            json.dump(self.all_product_data, file, indent=2, ensure_ascii=False)