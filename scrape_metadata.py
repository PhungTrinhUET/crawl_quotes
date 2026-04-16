import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

class MetadataScraper:
    """Extract text from meta tags and OpenGraph"""
    
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
    
    def extract_metadata(self, html: str) -> str:
        """Extract text from meta tags"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try OpenGraph description
            og_desc = soup.find('meta', {'property': 'og:description'})
            if og_desc and og_desc.get('content'):
                return og_desc.get('content')[:500]
            
            # Try meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc.get('content')[:500]
            
            # Try Twitter description
            twitter_desc = soup.find('meta', {'name': 'twitter:description'})
            if twitter_desc and twitter_desc.get('content'):
                return twitter_desc.get('content')[:500]
            
            # Fallback: get first 500 chars of first paragraph
            first_p = soup.find('p')
            if first_p:
                text = first_p.get_text().strip()
                return text[:500] if text else ''
        
        except:
            pass
        
        return ''
    
    def scrape(self, url: str) -> str:
        html = self.fetch_page(url)
        if not html:
            return ''
        return self.extract_metadata(html)

# Execute
df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].astype(str)

print('📥 Loading 2444 articles...')
print('🔍 Extracting metadata/descriptions...\n')

scraper = MetadataScraper()
total = len(df)
success_count = 0

for idx, row in df.iterrows():
    if idx % 50 == 0:
        print(f'[{idx+1:4d}/{total}] {row["title"][:40]}...')
    
    text = scraper.scrape(row['link'])
    if len(text) > 10:  # Only if we got substantial text
        df.at[idx, 'text'] = text
        success_count += 1
    
    if idx % 10 == 0:
        time.sleep(0.1)

df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
print(f'\n✅ CSV updated: data_cafe_enriched.csv')
print(f'   Extracted metadata: {success_count}/{total} articles')

with_text = df[df['text'].str.len() > 10]
print(f'\n📊 Results:')
print(f'   Total: {len(df)}')
print(f'   With text/metadata: {len(with_text)}')

if len(with_text) > 0:
    sample = with_text.iloc[0]
    print(f'\n📝 Sample:\n   Title: {sample["title"][:60]}...')
    print(f'   Desc:  {sample["text"][:100]}...')

# Update JSON
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
print(f'\n✅ JSON updated: data_cafe_enriched.json')
