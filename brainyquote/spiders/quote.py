import scrapy
from brainyquote.items import BrainyquoteItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['brainyquote.com']
    start_urls = [
        'https://www.brainyquote.com/topics'
    ]
    website_url = 'https://www.brainyquote.com'

    def parse(self, response):
        topic_links = response.selector.xpath('//a[contains(@href, "/topics/")]/@href').getall()

        for topic_link in topic_links:
            topic_link = self.website_url + topic_link
            yield scrapy.Request(topic_link, callback=self.parse_topic)


    def parse_topic(self, response):
        for quote_el in response.selector.xpath('//div[@id="quotesList"]//div[contains(@id, "pos_")]'):
            author = quote_el.xpath('.//a[@title="view author"]/text()').get()
            if author:
                item = BrainyquoteItem()
                item['author'] = author.strip()
                item['quote'] = quote_el.xpath('.//a[@title="view author"]/preceding-sibling::a/div/text()').get().strip()
                yield item