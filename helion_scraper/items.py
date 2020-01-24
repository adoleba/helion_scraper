import scrapy


class BookScrapyItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    price_category = scrapy.Field()
