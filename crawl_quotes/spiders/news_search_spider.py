"""
Multi-site Vietnamese news crawler for coffee-related articles.

This spider searches for coffee news across multiple Vietnamese news websites
(baomoi.com, vnexpress.net, vtcnews.vn, dantri.com.vn) and extracts articles
related to coffee, arabica, robusta, and agricultural commodities.

Features:
    - Multi-keyword search support
    - Coffee-related content filtering
    - Automatic link deduplication
    - Best-effort article metadata extraction
    - Support for multiple Vietnamese news sites

Usage:
    scrapy crawl news_search
    scrapy crawl news_search -a keywords="['cà phê', 'robusta']"
    python run_news_search.py "custom keyword" "another keyword"
"""

import scrapy
from urllib.parse import quote
from typing import Iterator, Dict, Optional, List


class NewsSearchSpider(scrapy.Spider):
    """Spider for crawling coffee-related news from Vietnamese news websites.
    
    Attributes:
        name (str): Spider identifier used by Scrapy
        allowed_domains (list): List of allowed domains to crawl
        seen_links (set): Global tracker for duplicate links
        coffee_keywords (list): Keywords used to filter coffee-related articles
    """
    
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

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Generate initial requests to search for coffee articles.
        
        Yields:
            scrapy.Request: Search requests to each site with pagination
        
        Note:
            - Baomoi: 50 pages per keyword
            - VnExpress: 30 pages per keyword
            - VTCNews: 30 pages per keyword
            - DanTri: 20 pages per keyword
        """
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

    def parse(self, response: scrapy.http.Response) -> Iterator[scrapy.Request | Dict]:
        """Route to site-specific parsers based on URL domain.
        
        Args:
            response (scrapy.http.Response): Response object from request
            
        Yields:
            scrapy.Request or Dict: Either requests to article pages or item dictionaries
        """
        url = response.url
        if 'baomoi.com' in url:
            yield from self.parse_baomoi(response)
        elif 'vnexpress' in url:
            yield from self.parse_vnexpress(response)
        elif 'vtcnews' in url:
            yield from self.parse_vtc(response)
        elif 'dantri' in url:
            yield from self.parse_dantri(response)
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

    def parse_baomoi(self, response: scrapy.http.Response) -> Iterator[Dict]:
        """Parse baomoi.com search results with coffee keyword filtering.
        
        Baomoi uses div.bm-card for article containers and includes metadata
        in the card footer (time, source).
        
        Args:
            response (scrapy.http.Response): Response from baomoi search page
            
        Yields:
            Dict: Article data (title, link, time, source, site)
        """
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

    def parse_article(self, response: scrapy.http.Response) -> Iterator[Dict]:
        """Extract article metadata from individual article pages.
        
        Attempts to extract title, publication time, and source from meta tags
        and HTML structure. Falls back through multiple selectors for robustness.
        
        Args:
            response (scrapy.http.Response): Response from article page
            
        Yields:
            Dict: Article data if coffee-related (title, link, time, source, site)
        """
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

    def _is_coffee_related(self, title: str) -> bool:
        """Check if title contains coffee-related keywords.
        
        Args:
            title (str): Article title to check
            
        Returns:
            bool: True if title contains any coffee keyword, False otherwise
        """
        if not title:
            return False
        title_lower = title.lower()
        # Check if any coffee keyword is in the title
        return any(keyword.lower() in title_lower for keyword in self.coffee_keywords)

    def parse_vnexpress(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        """Parse vnexpress.net search results.
        
        Attempts to find article containers using multiple selector strategies,
        with fallback to generic link extraction.
        
        Args:
            response (scrapy.http.Response): Response from vnexpress search page
            
        Yields:
            scrapy.Request: Requests to article pages for detailed parsing
        """
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
    
    def parse_vtc(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        """Parse vtcnews.vn search results.
        
        Attempts to find article containers using multiple selector strategies,
        with fallback to generic link extraction.
        
        Args:
            response (scrapy.http.Response): Response from vtcnews search page
            
        Yields:
            scrapy.Request: Requests to article pages for detailed parsing
        """
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

    def parse_dantri(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        """Parse dantri.com.vn search results.
        
        Similar strategy to vnexpress and vtcnews with multiple fallback selectors.
        
        Args:
            response (scrapy.http.Response): Response from dantri search page
            
        Yields:
            scrapy.Request: Requests to article pages for detailed parsing
        """
        # Try to find article items
        articles = response.css('article.article-item, div.story-item, div.article-box')
        if not articles:
            # Fallback: get all links that look like articles
            links = response.css('a[href*="/"]::attr(href)').getall()
            for href in links:
                if href and 'dantri' in href and 'tim-kiem' not in href:
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

    def _is_article_link(self, url: str, response: scrapy.http.Response) -> bool:
        """Check if URL looks like an article link (not pagination/search).
        
        Uses heuristics to filter out search pages, pagination links, and anchors.
        
        Args:
            url (str): URL to check
            response (scrapy.http.Response): Response object for domain matching
            
        Returns:
            bool: True if URL looks like an article, False otherwise
        """
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
