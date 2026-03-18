import scrapy
from urllib.parse import quote


class NewsSearchSpider(scrapy.Spider):
    name = "news_search"
    allowed_domains = ["baomoi.com", "vnexpress.net", "vtcnews.vn", "dantri.com.vn", "tinnhanhchungkhoan.vn"]

    # Keep seen links across whole run
    seen_links = set()
    
    # Coffee-related keywords for filtering
    coffee_keywords = [
        'cà phê', 'ca phe', 'coffee', 'robusta', 'arabica', 
        'tây nguyên', 'giá nông sản', 'xuất khẩu', 'cà-phê',
        'gia ca phe', 'nong san', 'dak lak', 'lam dong', 'gia lai'
    ]

    def start_requests(self):
        # Multiple coffee-related search keywords
        keywords = getattr(self, 'keywords', ['cà phê', 'robusta', 'arabica'])
        
        for keyword in keywords:
            q = quote(keyword, safe='')
            
            # Baomoi: 50 pages
            base_baomoi = f"https://baomoi.com/tim-kiem/{q}.epi"
            yield scrapy.Request(url=base_baomoi, callback=self.parse, meta={'keyword': keyword})
            for page in range(2, 51):
                yield scrapy.Request(url=f"https://baomoi.com/tim-kiem/{q}/trang{page}.epi", 
                                   callback=self.parse, meta={'keyword': keyword})

            # VnExpress: 30 pages
            for page in range(1, 31):
                yield scrapy.Request(url=f"https://vnexpress.net/tim-kiem?q={q}&p={page}", 
                                   callback=self.parse, meta={'keyword': keyword})

            # VTCNews: 30 pages
            for page in range(1, 31):
                yield scrapy.Request(url=f"https://vtcnews.vn/tim-kiem?q={q}&p={page}", 
                                   callback=self.parse, meta={'keyword': keyword})
            
            # DanTri: 20 pages (if search works)
            for page in range(1, 21):
                yield scrapy.Request(url=f"https://dantri.com.vn/tim-kiem?q={q}&p={page}", 
                                   callback=self.parse, meta={'keyword': keyword})

    def parse(self, response):
        url = response.url
        if 'baomoi.com' in url:
            yield from self.parse_baomoi(response)
        elif 'vnexpress' in url:
            yield from self.parse_vnexpress(response)
        elif 'vtcnews' in url:
            yield from self.parse_vtc(response)
        else:
            # Generic listing parsing for other sites
            links = response.css('a[href]::attr(href)').getall()
            for href in links:
                if not href:
                    continue
                full = response.urljoin(href)
                if self._is_article_link(full, response):
                    if full not in self.seen_links:
                        self.seen_links.add(full)
                        yield scrapy.Request(full, callback=self.parse_article)

    def parse_baomoi(self, response):
        articles = response.css('div.bm-card')
        for article in articles:
            title = article.css('a[title]::attr(title)').get()
            link = article.css('a[href]::attr(href)').get()
            time = article.css('div.bm-card-footer time::attr(datetime)').get()
            if not time:
                time = article.css('div.bm-card-footer time::text').get()
            source = article.css('div.bm-card-footer a::attr(title)').get()

            if title and link and self._is_coffee_related(title):
                full = response.urljoin(link)
                if full not in self.seen_links:
                    self.seen_links.add(full)
                    yield {
                        'title': title.strip(),
                        'link': full,
                        'time': time.strip() if time else 'Không rõ',
                        'source': source.strip() if source else 'baomoi',
                        'site': 'baomoi.com'
                    }

    def parse_article(self, response):
        # Best-effort extraction from article page
        title = response.css('h1::text').get()
        if not title:
            title = response.css('meta[property="og:title"]::attr(content)').get()
        if not title:
            title = response.css('title::text').get()

        time = response.css('time::attr(datetime)').get()
        if not time:
            time = response.css('meta[property="article:published_time"]::attr(content)').get()

        site = response.url.split('/')[2] if response.url else ''
        source = site

        # Filter by coffee-related keywords in title
        if title and title.strip() and self._is_coffee_related(title):
            yield {
                'title': title.strip(),
                'link': response.url,
                'time': time.strip() if time else 'Không rõ',
                'source': source,
                'site': site
            }

    def _is_coffee_related(self, title):
        """Check if title contains coffee-related keywords."""
        if not title:
            return False
        title_lower = title.lower()
        # Check if any coffee keyword is in the title
        return any(keyword.lower() in title_lower for keyword in self.coffee_keywords)


    def parse_vnexpress(self, response):
        """Parse vnexpress search results or article list."""
        # Try to find article items (vnexpress may use different selectors)
        articles = response.css('article.item-news, div.item-news, a.txt-link-article')
        if not articles:
            # Fallback: get all links that look like articles
            links = response.css('a[href*="/"]::attr(href)').getall()
            for href in links:
                if href and 'vnexpress' in href and 'tim-kiem' not in href:
                    full = response.urljoin(href)
                    if full not in self.seen_links:
                        self.seen_links.add(full)
                        yield scrapy.Request(full, callback=self.parse_article)
        else:
            for article in articles:
                link = article.css('a::attr(href)').get()
                if link:
                    full = response.urljoin(link)
                    if full not in self.seen_links:
                        self.seen_links.add(full)
                        yield scrapy.Request(full, callback=self.parse_article)
    
    def parse_vtc(self, response):
        """Parse vtcnews search results or article list."""
        # Try to find article containers (vtcnews may use different selectors)
        articles = response.css('div.story-item, article.story, div.news-item')
        if not articles:
            # Fallback: get all links that look like articles
            links = response.css('a[href*="/"]::attr(href)').getall()
            for href in links:
                if href and 'vtcnews' in href and 'tim-kiem' not in href:
                    full = response.urljoin(href)
                    if full not in self.seen_links:
                        self.seen_links.add(full)
                        yield scrapy.Request(full, callback=self.parse_article)
        else:
            for article in articles:
                link = article.css('a::attr(href)').get()
                if link:
                    full = response.urljoin(link)
                    if full not in self.seen_links:
                        self.seen_links.add(full)
                        yield scrapy.Request(full, callback=self.parse_article)

    def _is_article_link(self, url, response):
        # Heuristics to avoid search/listing/pagination links
        if 'tim-kiem' in url or 'page' in url or url.endswith('#'):
            return False
        # Only keep links on the same domain
        if response.url.split('/')[2] not in url:
            return False
        # Common pattern: article links are longer and often contain a hyphen or date
        if '-' in url or any(segment.isdigit() and len(segment) >= 3 for segment in url.split('/')):
            return True
        # Last resort: allow if link path length is > 3
        return len(url.split('/')) > 4
