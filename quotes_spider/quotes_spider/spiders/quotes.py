import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']
    counter = 0

    def parse(self, response):

        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first()
            self.counter = self.counter + 1

            yield { 'author': author, 'text': text, 'tags': tags }
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        absulate_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absulate_next_page_url)
