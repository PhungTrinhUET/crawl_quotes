import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class SmartScraper:
    """Smart scraper - text + fallback to title"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    
    def fetch(self, url: str, timeout=8):
        try:
            resp = requests.get(url, headers=self.headers, timeout=timeout)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                return resp.text
        except:
            pass
        return None
    
    def scrape_url(self, url: str, title: str = '') -> str:
        """Scrape with fallback to title"""
        html = self.fetch(url)
        if not html:
            return title  # Use title as fallback
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try to find paragraphs in article
            article = soup.find('article') or \
                     soup.find('div', class_=re.compile(r'article|content', re.I))
            
            paras = []
            if article:
                paras = [p.get_text().strip() for p in article.find_all('p') if len(p.get_text().strip()) > 15]
            
            if not paras:
                # Get all p tags
                paras = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 15]
            
            if paras:
                text = ' '.join(paras[:8])
                text = re.sub(r'\s+', ' ', text).strip()
                # Check if it's actual text (not URL, not too short)
                if len(text) > 50 and 'http' not in text[:100]:
                    return text[:500]
            
            # If no text extracted, return title
            return title
        
        except:
            return title

# Load data
df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].fillna('')

print(f'🚀 Smart scraping {len(df)} articles (with fallback to title)...\n')

scraper = SmartScraper()
text_results = [''] * len(df)
start_time = time.time()

# Parallel execution
with ThreadPoolExecutor(max_workers=16) as executor:
    futures = {
        executor.submit(scraper.scrape_url, df.iloc[idx]['link'], df.iloc[idx]['title']): idx 
        for idx in range(len(df))
    }
    
    for i, future in enumerate(as_completed(futures)):
        idx = futures[future]
        try:
            text_results[idx] = future.result()
        except:
            text_results[idx] = df.iloc[idx]['title']  # Fallback to title
        
        # Progress
        if (i + 1) % 200 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (len(df) - i - 1) / rate if rate > 0 else 0
            print(f'[{i+1:4d}/{len(df)}] ETA: {remaining:3.0f}s')

# Assign
df['text'] = text_results
elapsed = time.time() - start_time

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')

# Stats
with_actual_text = df[~df['text'].str.contains(df['title'], case=False, regex=False)]
print(f'\n✅ Complete in {elapsed:.1f}s')
print(f'   Total: {len(df)}')
print(f'   With actual text: {len(with_actual_text)} ({len(with_actual_text)*100/len(df):.1f}%)')
print(f'   With title fallback: {len(df) - len(with_actual_text)}')

# Samples
print(f'\n📝 Sample (with actual text):\n')
for idx, row in with_actual_text.head(2).iterrows():
    print(f'{idx+1}. {row["title"][:65]}...')
    print(f'   Text: {row["text"][:90]}...\n')

# JSON
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
print(f'✅ Saved: data_cafe_enriched.csv & .json')
