import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

class AdvancedArticleScraper:
    """Improved article scraper with multiple fallback selectors"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self, url: str):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except:
            return None
    
    def extract_generic(self, html: str) -> str:
        """Generic extraction with multiple selector fallbacks"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try multiple selectors
            selectors = [
                ('div[class*="article-content"]', 'p'),
                ('div[class*="content"]', 'p'),
                ('article', 'p'),
                ('div[class*="story"]', 'p'),
                ('div[id*="content"]', 'p'),
                ('main', 'p'),
            ]
            
            for container_selector, para_selector in selectors:
                try:
                    container = soup.select_one(container_selector)
                    if container:
                        paragraphs = container.select(para_selector)
                        if paragraphs and len(paragraphs) > 0:
                            text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                            if len(text) > 50:
                                return text[:500]
                except:
                    pass
            
            # Fallback: get all paragraphs
            paragraphs = soup.find_all('p')
            if paragraphs and len(paragraphs) > 5:
                text = ' '.join([p.get_text().strip() for p in paragraphs[:10]])
                return text[:500] if len(text) > 50 else ''
        
        except:
            pass
        
        return ''
    
    def scrape(self, url: str) -> str:
        html = self.fetch_page(url)
        if not html:
            return ''
        return self.extract_generic(html)

# Execute
df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].astype(str)

print(f'📥 Loaded {len(df)} records')
print(f'🔍 Scraping first 100 articles...\n')

scraper = AdvancedArticleScraper()
total = min(100, len(df))
success_count = 0

for idx, row in df.head(total).iterrows():
    if idx % 10 == 0:
        print(f'[{idx+1:3d}/{total}] {row["title"][:45]}...')
    
    text = scraper.scrape(row['link'])
    if len(text) > 0:
        df.at[idx, 'text'] = text
        success_count += 1
    
    if idx % 5 == 0:
        time.sleep(0.2)

df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
print(f'\n✅ Updated: data_cafe_enriched.csv')
print(f'   Scraped: {success_count}/{total} articles')

with_text = df[df['text'].str.len() > 0]
print(f'\n📊 Results: {len(with_text)} articles with text')

if len(with_text) > 0:
    sample = with_text.iloc[0]
    print(f'\n📝 Sample:\n  {sample["text"][:100]}...')

# Update JSON
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
print(f'\n✅ Updated: data_cafe_enriched.json')
