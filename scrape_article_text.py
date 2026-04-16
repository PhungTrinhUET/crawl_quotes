import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from typing import Optional

class ArticleScraper:
    """Scrape article text from various Vietnamese news websites"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"  ❌ Error fetching {url}: {str(e)[:50]}")
            return None
    
    def extract_baomoi(self, html: str) -> str:
        """Extract article text from baomoi.com"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Look for article content div
            article = soup.find('div', {'class': 'article-text'})
            if not article:
                article = soup.find('article')
            if not article:
                article = soup.find('div', {'id': 'article-content'})
            
            if article:
                paragraphs = article.find_all('p')
                text = '\n'.join([p.get_text().strip() for p in paragraphs])
                return text[:500] if text else ''  # First 500 chars
        except:
            pass
        return ''
    
    def extract_vnexpress(self, html: str) -> str:
        """Extract article text from vnexpress.net"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # VnExpress uses article class
            article = soup.find('article')
            if not article:
                article = soup.find('div', {'class': ['fck_detail', 'article-content']})
            
            if article:
                paragraphs = article.find_all('p')
                text = '\n'.join([p.get_text().strip() for p in paragraphs])
                return text[:500] if text else ''
        except:
            pass
        return ''
    
    def extract_vtcnews(self, html: str) -> str:
        """Extract article text from vtcnews.vn"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # VTC uses different structure
            article = soup.find('div', {'class': ['article-content', 'article-body']})
            if not article:
                article = soup.find('article')
            
            if article:
                paragraphs = article.find_all('p')
                text = '\n'.join([p.get_text().strip() for p in paragraphs])
                return text[:500] if text else ''
        except:
            pass
        return ''
    
    def extract_dantri(self, html: str) -> str:
        """Extract article text from dantri.com.vn"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find('div', {'class': ['article-content', 'content']})
            if not article:
                article = soup.find('article')
            
            if article:
                paragraphs = article.find_all('p')
                text = '\n'.join([p.get_text().strip() for p in paragraphs])
                return text[:500] if text else ''
        except:
            pass
        return ''
    
    def scrape(self, url: str, site: str) -> str:
        """Scrape article text based on site"""
        html = self.fetch_page(url)
        if not html:
            return ''
        
        if 'baomoi' in site.lower():
            return self.extract_baomoi(html)
        elif 'vnexpress' in site.lower():
            return self.extract_vnexpress(html)
        elif 'vtcnews' in site.lower():
            return self.extract_vtcnews(html)
        elif 'dantri' in site.lower():
            return self.extract_dantri(html)
        
        return ''

# Load enriched data
df = pd.read_csv('data_cafe_enriched.csv')

# Ensure text column is string type
df['text'] = df['text'].astype(str)

print(f'📥 Loaded {len(df)} records')
print(f'🔍 Scraping article text (first 50 for demo)...\n')

scraper = ArticleScraper()
total = min(50, len(df))  # Scrape first 50 for demo
text_list = []

for idx, row in df.head(total).iterrows():
    print(f'[{idx+1}/{total}] {row["title"][:50]}...')
    text = scraper.scrape(row['link'], row['site'])
    text_list.append(text)
    time.sleep(0.5)  # Be respectful

# Update text column
df.loc[df.index[:total], 'text'] = text_list

# Save updated data
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
print(f'\n✅ CSV updated: data_cafe_enriched.csv')

# Convert to JSON
json_data = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
print(f'✅ JSON updated: data_cafe_enriched.json')

# Show sample
print('\n📋 Sample with text:\n')
sample = df[df['text'].str.len() > 0].iloc[0] if any(df['text'].str.len() > 0) else df.iloc[0]
print(f"Title: {sample['title']}")
print(f"Link:  {sample['link']}")
print(f"Text:  {sample['text'][:100]}...")
