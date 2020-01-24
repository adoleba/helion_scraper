import scrapy

from helion_scraper.items import BookScrapyItem


class BookItemScraperSpider(scrapy.Spider):
    name = 'book_item'
    allowed_domains = ['helion.pl']
    start_urls = ['https://helion.pl/kategorie/programowanie']

    def parse(self, response):

        books = response.css('li.classPresale')

        for book in books:
            title = book.css('div.book-info > div.book-info-middle > h3 > a::text').extract_first()
            author = book.css('div.book-info > div.book-info-middle > p > a::text').extract_first()
            price = book.css('p.price-add > a > span::text').extract_first()

            book_items = BookScrapyItem()
            book_items["title"] = title
            book_items['author'] = author
            book_items['price'] = price

            yield book_items