import scrapy
from scrapy.crawler import CrawlerProcess

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
            special_price = book.css('p.price > a > ins > span::text').extract_first()

            book_items = BookScrapyItem()
            book_items["title"] = title
            book_items['author'] = author
            if price is not None:
                book_items['price'] = price.strip(' zł').replace('.', ',')
            elif special_price is not None:
                book_items['price'] = special_price.strip(' zł').replace('.', ',')
            else:
                book_items['price'] = 'produkt chwilowo niedostępny'

            if ',' in book_items['price']:
                book_price = float(book_items['price'].replace(',', '.'))
                if book_price < 50:
                    book_items['price_category'] = '< 50 zł'
                elif 100 > book_price >= 50:
                    book_items['price_category'] = '50 - 100 zł'
                elif 150 > book_price >= 100:
                    book_items['price_category'] = '100 - 150 zł'
                else:
                    book_items['price_category'] = '> 150 zł'
            else:
                book_items['price_category'] = 'produkt chwilowo niedostępny'

            yield book_items

        next_page = response.css('div.stronicowanie > a:last-child::text').extract()
        next_page_url = response.css('div.stronicowanie > a:last-child::attr(href)').get()

        if '>' in next_page:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_URI': 'spider.csv',
        'FEED_FORMAT': 'csv'
    })
    process.crawl(BookItemScraperSpider)
    process.start()
