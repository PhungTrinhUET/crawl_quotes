import scrapy

class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        # Tìm tất cả các khối chứa câu nói
        quotes = response.css('.quote')
        
        for quote in quotes:
            # Lấy nội dung câu trích dẫn và tên tác giả
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            
            # Trả về kết quả
            yield {
                'text': text,
                'author': author
            }