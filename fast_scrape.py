import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class FastTextScraper:
    """Fast parallel text extraction"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Accept-Language': 'vi,en;q=0.9',
        }
    
    def fetch(self, url: str, timeout=8):
        """Fetch page"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=timeout)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                return resp.text
        except:
            pass
        return None
    
    def extract_text(self, html: str) -> str:
        """Extract text from HTML"""
        if not html:
            return ''
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Skip if HTML is too small (likely error page)
            if len(html) < 5000:
                return ''
            
            # Try article content - multiple selector strategies
            article = None
            
            # Try common article containers
            selectors = [
                soup.find('article'),
                soup.find('div', class_=re.compile(r'article-content', re.I)),
                soup.find('div', class_=re.compile(r'article-body', re.I)),
                soup.find('div', class_=re.compile(r'post-content', re.I)),
                soup.find('div', id=re.compile(r'article', re.I)),
                soup.find('div', id=re.compile(r'content', re.I)),
            ]
            
            for sel in selectors:
                if sel:
                    article = sel
                    break
            
            # If found article container, extract paragraphs
            if article:
                paras = article.find_all('p', limit=8)
                if len(paras) >= 2:
                    text = ' '.join([p.get_text().strip() for p in paras if len(p.get_text().strip()) > 20])
                    text = re.sub(r'\s+', ' ', text).strip()
                    # Skip if too short or is a URL
                    if len(text) > 50 and 'http' not in text[:100]:
                        return text[:500]
            
            # Fallback: all paragraphs on page
            all_paras = soup.find_all('p')
            # Get paragraphs that are substantial (skip very short ones)
            good_paras = [p for p in all_paras[:15] if len(p.get_text().strip()) > 20]
            
            if len(good_paras) >= 3:
                text = ' '.join([p.get_text().strip() for p in good_paras[:8]])
                text = re.sub(r'\s+', ' ', text).strip()
                # Skip if URL
                if len(text) > 50 and 'http' not in text[:100]:
                    return text[:500]
        
        except Exception as e:
            pass
        
        return ''
    
    def scrape_url(self, url: str) -> str:
        """Scrape single URL"""
        html = self.fetch(url)
        return self.extract_text(html) if html else ''

# Load and prepare data
df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].fillna('')
df['text'] = df['text'].astype(str)

print(f'🚀 Parallel scraping {len(df)} articles with 16 workers...\n')

scraper = FastTextScraper()
text_results = [''] * len(df)
start_time = time.time()

# Execute parallel scraping
with ThreadPoolExecutor(max_workers=16) as executor:
    futures = {
        executor.submit(scraper.scrape_url, url): idx 
        for idx, url in enumerate(df['link'])
    }
    
    completed = 0
    for i, future in enumerate(as_completed(futures)):
        idx = futures[future]
        try:
            text = future.result()
            text_results[idx] = text if text else ''
            if len(text) > 0:
                completed += 1
        except Exception as e:
            text_results[idx] = ''
        
        # Progress every 200 items
        if (i + 1) % 200 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (len(df) - i - 1) / rate if rate > 0 else 0
            print(f'[{i+1:4d}/{len(df)}] Success: {completed:4d} | ETA: {remaining:3.0f}s')

# Assign results
df['text'] = text_results
elapsed = time.time() - start_time

# Save files
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')

# Stats
with_text = df[df['text'].str.len() > 0]
print(f'\n✅ Complete in {elapsed:.1f}s')
print(f'   Success: {len(with_text)}/{len(df)} ({len(with_text)*100/len(df):.1f}%)')

# Samples
print(f'\n📝 Sample articles with text:\n')
for idx, row in with_text.head(3).iterrows():
    print(f'{idx+1}. {row["title"][:65]}...')
    print(f'   Text: {row["text"][:90]}...\n')

# JSON
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
print(f'✅ Saved: data_cafe_enriched.csv & .json')
