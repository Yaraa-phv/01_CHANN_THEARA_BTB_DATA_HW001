import scrapy
import time
from scrapy_selenium import SeleniumRequest 
from selenium.webdriver.common.by import By

class ScrappingSpider(scrapy.Spider):
    name = "scrap_testiminials"
    allowed_domains = ["web-scraping.dev"]
    # start_urls = ["https://web-scraping.dev/login?cookies="]

    def start_requests(self):
        url = "https://web-scraping.dev/login?cookies="

        yield SeleniumRequest(
            url = url,
            callback = self.parse
        )
        # return super().start_requests()

    # func for handle cookie by click Ok and submit login
    def parse(self, response):
        driver = response.meta['driver']
        self.logger.info(f"Meta keys: {list(response.meta.keys())}")
        time.sleep(2)

        if not driver:
            self.logger.error("No 'driver' in response.meta. Did you use SeleniumRequest?")
            return

        cookie_button = driver.find_element(By.XPATH, '//*[@id="cookie-ok"]')
        cookie_button.click()
        time.sleep(2)

        username_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[1]/input[@name="username"]')
        username_input.send_keys('user123')
        time.sleep(2)

        password = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/div[2]/input[@name="password"]')
        password.send_keys('password')
        time.sleep(2)

        click_submit = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/button[@type="submit"]')
        click_submit.click()
        time.sleep(2)

        # Another way to click on testiminial nav
        # click_testiminial_nav = driver.find_element(By.XPATH, '//*[@id="navbarContent"]/ul[1]/li[4]/a')
        # click_testiminial_nav.click()
        # time.sleep(2)

        # move to testiminial nav by link
        testiminial_url = 'https://web-scraping.dev/testimonials'
        yield SeleniumRequest(
            url = testiminial_url,
            callback = self.scroll_testiminials,
            wait_time=2
        )

    def scroll_testiminials(self, response):
        driver = response.meta['driver']
        time.sleep(3)
    
        # scroll down until no more content loading
        # from stackoverflow
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # get all testimonial cards
        testimonial_cards = driver.find_elements(By.CLASS_NAME, "testimonial")

        #loop each card to get the rating and text
        for card in testimonial_cards:
            # count the length of <svg> to be as the num of rating
            rating = len(card.find_elements(By.CSS_SELECTOR, ".rating svg"))
            text = card.find_element(By.CLASS_NAME, "text").text.strip()

            yield {
                'rating': rating,
                'text': text
            }