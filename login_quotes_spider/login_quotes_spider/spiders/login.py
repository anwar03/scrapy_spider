import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        yield FormRequest('https://quotes.toscrape.com/login',
                          formdata={'csrf_token': csrf_token,
                                    'username': 'foobar',
                                    'password': 'foobar'
                                    },
                          callback=self.parse_after_login,
                          )

    def parse_after_login(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first()

            yield { 'author': author, 'text': text, 'tags': tags }
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absulate_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absulate_next_page_url, self.parse_after_login)
