import scrapy
from scrapy.http import Request


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absulate_url = response.urljoin(book)
            yield Request(absulate_url, callback=self.parse_book)

        # process next page
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()
        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')
        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        udc = response.xpath('//th[text()="UPC"]/following-sibling::td/text()').extract_first()
        product_ype = response.xpath('//th[text()="Product Type"]/following-sibling::td/text()').extract_first()
        price_excl = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()').extract_first()
        price_incl = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()').extract_first()
        tax = response.xpath('//th[text()="Tax"]/following-sibling::td/text()').extract_first()
        availability = response.xpath('//th[text()="Availability"]/following-sibling::td/text()').extract_first()
        number_of_reviews = response.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()').extract_first()

        yield {
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            "udc": udc,
            "product_ype": product_ype,
            "price_excl": price_excl,
            "price_incl": price_incl,
            "tax": tax,
            "availability": availability,
            "number_of_reviews": number_of_reviews
        }
