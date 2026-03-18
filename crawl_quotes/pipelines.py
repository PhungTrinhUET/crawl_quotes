# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy


class CrawlQuotesPipeline:
    def process_item(self, item, spider):
        return item


class DedupePipeline:
    """Drop items with duplicate 'link' values."""
    
    def __init__(self):
        self.seen_links = set()
    
    def process_item(self, item, spider):
        link = item.get('link')
        if link:
            if link in self.seen_links:
                raise scrapy.exceptions.DropItem(f'Duplicate link: {link}')
            self.seen_links.add(link)
        return item
