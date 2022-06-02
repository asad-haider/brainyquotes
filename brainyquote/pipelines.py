# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from datetime import datetime
from itemadapter import ItemAdapter


class BrainyquotePipeline:

    def __init__(self, settings):

        connection_string = settings.get('MONGO_URL')
        database_name = settings.get('MONGO_DATABASE')
        quote_col_name = settings.get('MONGO_COLLECTION')
  
        self.connection = pymongo.MongoClient(connection_string)
        self.database = self.connection.get_database(database_name)
        self.quotes_col = self.database.get_collection(quote_col_name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        item['crawled_at'] = datetime.now()
        self.quotes_col.insert_one({
            'quote': item['quote'],
            'author': item['author'],
            'crawled_at': item['crawled_at']
        })
        return item
