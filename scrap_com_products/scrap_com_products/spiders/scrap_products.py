import scrapy
from scrap_com_products.items import ScrapComProductsItem


class ScrapProductsSpider(scrapy.Spider):
    name = "scrap_products"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/"]

    def parse(self, response):
        
        # Get category links
        links = response.xpath('//*[@id="res-menu"]/ul/li/a')
        # print(f'Found {len(links)} of total links')

        for link in links:
            category = link.xpath('string(.)').get(default='No Category').strip()
            url = link.xpath('@href').get()

            # Skip unwanted categories
            unwanted = ['home', 'contact', 'about']
            
            if not category or not url or category.lower() in unwanted:
                print(f"Skipping none category or url : {category}")
                continue

            # print(f"=====> Processing category: {category}")
            
            yield scrapy.Request(
                url=url,
                callback=self.parse_category_page,
                meta={'category': category}
            )

    def parse_category_page(self, response):
        category = response.meta['category']
        
        product_links = []
        
        detail_links = response.xpath('//div[contains(@class, "product-thumb")]//h4/a/@href').getall()
        if detail_links:
            product_links = detail_links
            print(f"Found {len(detail_links)} product detail_links")

        for product_url in product_links:
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product_detail,
                meta={'category': category}
            )

        next_page = response.xpath('//ul[@class="pagination"]//a[contains(text(), ">")]/@href').get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_category_page,
                meta={'category': category}
            )

    def parse_product_detail(self, response):
        category = response.meta['category']
        title = response.xpath('//div[@id="content"]//h3/text()').get(default='No Title').strip()
        brand = response.xpath('//ul[@class="list-unstyled"]/li[span[text()="Brand:"]]/a/text()').get(default='No Brand').strip()
        code = response.xpath('//ul[@class="list-unstyled"]/li[span[text()="Product Code:"]]/text()').get(default='No Code').replace('Product Code:', '').strip()
        price = response.xpath('//ul[@class="list-unstyled price"]/li/h3/text()').get(default='No Price').strip()
        image_link = response.xpath('//a[@class="thumbnail"]/@href').get()
        if not image_link:
            image_link = response.xpath('//*[@id="content"]/div[1]/div[1]/div/div/div//img/@src').get()
        review = response.xpath('//a[contains(@class, "review-count")]/text()').get(default='No Review').strip()
        
        # Create the item
        item = ScrapComProductsItem(
            category=category,
            product_data={
                'category' : category,
                'title': title,
                'brand': brand,
                'code': code,
                'price': price,
                'image_link': image_link,
                'review': review,
            }
        )
        
        yield item