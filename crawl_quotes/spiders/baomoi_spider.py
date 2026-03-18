import scrapy

class BaomoiSpiderSpider(scrapy.Spider):
    name = "baomoi_spider"
    allowed_domains = ["baomoi.com"]
    
    # BỘ NHỚ TẠM: Đặt ở ngoài cùng để nhớ link chống trùng lặp qua tất cả 10 trang
    seen_links = set()

    def start_requests(self):
        # 1. Quét trang đầu tiên (link không có chữ "trang")
        yield scrapy.Request(url="https://baomoi.com/tim-kiem/xăng.epi", callback=self.parse)
        
        # 2. Vòng lặp quét từ trang 2 đến trang 10 (bạn có thể đổi số 11 thành số lớn hơn nếu muốn)
        base_url = "https://baomoi.com/tim-kiem/xăng/trang{}.epi" 
        for page in range(2, 11): 
            url = base_url.format(page) 
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Bắt "Khung lớn" của từng bài báo
        articles = response.css('div.bm-card') 
        
        for article in articles:
            # Nhặt thông tin bên trong
            title = article.css('a[title]::attr(title)').get()
            link = article.css('a[href]::attr(href)').get()
            
            time = article.css('div.bm-card-footer time::attr(datetime)').get()
            if not time:
                time = article.css('div.bm-card-footer time::text').get()
                
            source = article.css('div.bm-card-footer a::attr(title)').get()

            if title and link:
                full_link = response.urljoin(link)
                
                # Kiểm tra trùng lặp
                if full_link not in self.seen_links:
                    self.seen_links.add(full_link) 
                    
                    yield {
                        'title': title.strip(),
                        'link': full_link,
                        'time': time.strip() if time else 'Không rõ',
                        'source': source.strip() if source else 'Không rõ'
                    }