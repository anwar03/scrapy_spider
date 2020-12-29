from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from books_crawler.items import BooksCrawlerItem

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    # start_urls = ['https://books.toscrape.com/']

    def start_requests(self):
        self.driver = webdriver.Chrome('/home/karigor/chromedriver')
        self.driver.get('https://books.toscrape.com')

        self.sel = Selector(text=self.driver.page_source)
        books = self.sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'https://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)

        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds...')
                next_page.click()


                self.sel = Selector(text=self.driver.page_source)
                books = self.sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'https://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('No nore pages to load..')
                self.driver.quit()
                break

    def parse_book(self, response):
        items = BooksCrawlerItem()
        title = response.css('h1::text').extract_first()
        url = response.request.url

        items['title'] = title
        items['url'] = url

        yield items
