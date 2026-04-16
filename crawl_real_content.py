import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class ContentScraper:
    """Advanced scraper focused on actual article content"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Accept-Language': 'vi,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
    
    def fetch(self, url: str, timeout=10):
        """Fetch with better error handling"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=timeout)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                return resp.text
        except:
            pass
        return None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        # Remove email
        text = re.sub(r'\S+@\S+', '', text)
        return text.strip()
    
    def scrape_content(self, html: str) -> str:
        """Extract article content (not title/headline)"""
        if not html or len(html) < 3000:
            return ''
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script, style, nav, header elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try different article container strategies
            article_content = None
            
            # Strategy 1: article tag
            article_content = soup.find('article')
            
            # Strategy 2: div with article class patterns
            if not article_content:
                patterns = ['article-content', 'article-body', 'post-content', 'entry-content', 'content-body']
                for pattern in patterns:
                    article_content = soup.find('div', class_=re.compile(pattern, re.I))
                    if article_content:
                        break
            
            # Strategy 3: div with id patterns
            if not article_content:
                patterns = ['article', 'content', 'main-content', 'post', 'entry']
                for pattern in patterns:
                    article_content = soup.find('div', id=re.compile(pattern, re.I))
                    if article_content:
                        break
            
            # Strategy 4: main tag
            if not article_content:
                article_content = soup.find('main')
            
            # Extract paragraphs
            content_text = ''
            if article_content:
                paragraphs = article_content.find_all('p')
                # Filter out very short paragraphs (likely navigation/metadata)
                meaningful_paras = [p.get_text().strip() for p in paragraphs 
                                  if len(p.get_text().strip()) > 30]
                
                if meaningful_paras:
                    content_text = ' '.join(meaningful_paras)
            
            # Fallback: get all substantial paragraphs
            if not content_text or len(content_text) < 100:
                all_paras = soup.find_all('p')
                meaningful_paras = [p.get_text().strip() for p in all_paras 
                                  if len(p.get_text().strip()) > 30]
                if len(meaningful_paras) >= 3:
                    content_text = ' '.join(meaningful_paras[:15])
            
            # Clean and return
            if content_text:
                content_text = self.clean_text(content_text)
                # Return max 800 chars of actual content
                if len(content_text) > 100:
                    return content_text[:800]
        
        except:
            pass
        
        return ''
    
    def scrape(self, url: str) -> str:
        """Main scrape function"""
        html = self.fetch(url)
        if html:
            return self.scrape_content(html)
        return ''

# Load data
df = pd.read_csv('data_cafe_enriched.csv')
print(f'🚀 Crawling actual article content for {len(df)} articles...\n')

scraper = ContentScraper()
content_results = [''] * len(df)
start_time = time.time()

# Parallel scraping
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {
        executor.submit(scraper.scrape, url): idx 
        for idx, url in enumerate(df['link'])
    }
    
    success_count = 0
    for i, future in enumerate(as_completed(futures)):
        idx = futures[future]
        try:
            content = future.result()
            content_results[idx] = content
            if len(content) > 100:
                success_count += 1
        except:
            content_results[idx] = ''
        
        # Progress
        if (i + 1) % 300 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (len(df) - i - 1) / rate if rate > 0 else 0
            print(f'[{i+1:4d}/{len(df)}] Success: {success_count:4d} | ETA: {remaining:3.0f}s')

elapsed = time.time() - start_time

# Assign results
df['content_text'] = content_results

# Create summary from content_text, fallback to title if needed
summaries = []
for idx, row in df.iterrows():
    content = row['content_text']
    
    if len(content) > 50:  # Use actual content
        summary = content[:150]
        if len(content) > 150:
            summary = summary.rsplit(' ', 1)[0] + '...'
    else:  # Fallback to title + first few words of content
        summary = row['title'][:150]
    
    summaries.append(summary)

df['summary'] = summaries

# Reorder columns
column_order = ['title', 'summary', 'content_text', 'link', 'time', 'category', 'source', 'site']
df = df[column_order]

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

# Stats
with_content = df[df['content_text'].str.len() > 100]
print(f'\n✅ Complete in {elapsed:.1f}s')
print(f'   Success: {len(with_content)}/{len(df)} ({len(with_content)*100/len(df):.1f}%)')

# Samples
print(f'\n📝 Sample articles with real content:\n')
for idx, row in with_content.head(2).iterrows():
    print(f'{idx+1}. Title: {row["title"][:60]}...')
    print(f'   Content: {row["content_text"][:100]}...\n')

print(f'✅ Saved: data_cafe_enriched.csv & .json')
