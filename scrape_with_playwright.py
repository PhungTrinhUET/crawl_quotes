import pandas as pd
from playwright.async_api import async_playwright
import asyncio
import re

class PlaywrightScraper:
    """Scraper using Playwright for JavaScript-rendered content"""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        return text.strip()
    
    async def scrape_url(self, browser, url: str) -> str:
        """Scrape single URL"""
        try:
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=15000)
            
            # Wait for content to load
            await page.wait_for_timeout(2000)
            
            # Try to extract article content
            selectors = [
                'article p',
                'div.article-content p',
                'div.article-body p',
                'div[class*="content"] p',
                'main p',
                'p',
            ]
            
            content_text = ''
            for selector in selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements and len(elements) >= 3:
                        texts = []
                        for elem in elements[:15]:
                            text = await elem.text_content()
                            if text and len(text.strip()) > 30:
                                texts.append(text.strip())
                        
                        if texts:
                            content_text = ' '.join(texts)
                            break
                except:
                    pass
            
            # Clean and return
            if content_text:
                content_text = self.clean_text(content_text)
                if len(content_text) > 100:
                    await context.close()
                    return content_text[:800]
            
            await context.close()
            return ''
        
        except Exception as e:
            return ''
    
    async def scrape_batch(self, urls: list) -> list:
        """Scrape multiple URLs"""
        results = [''] * len(urls)
        
        async with async_playwright() as p:
            # Use single browser instance
            browser = await p.chromium.launch(headless=True)
            
            # Sequential scraping (parallel would be too memory-intensive)
            for idx, url in enumerate(urls):
                if (idx + 1) % 100 == 0:
                    print(f'[{idx+1}/{len(urls)}] scraped')
                
                result = await self.scrape_url(browser, url)
                results[idx] = result
            
            await browser.close()
        
        return results

# Load data
df = pd.read_csv('data_cafe_enriched.csv')
print(f'🚀 Scraping {len(df)} articles with Playwright (JavaScript support)...\n')
print('⏱️  This will take ~5-10 minutes (rendering each page)...\n')

scraper = PlaywrightScraper()

# Run async scraper
async def main():
    return await scraper.scrape_batch(df['link'].tolist())

import time
start = time.time()

# Use asyncio.run for Python 3.7+
try:
    content_results = asyncio.run(main())
except RuntimeError:
    # Fallback for already-running event loop
    loop = asyncio.get_event_loop()
    content_results = loop.run_until_complete(main())

elapsed = time.time() - start

# Assign results
df['content_text'] = content_results

# Create summary
summaries = []
for idx, row in df.iterrows():
    content = row['content_text']
    
    if len(content) > 50:
        summary = content[:150]
        if len(content) > 150:
            summary = summary.rsplit(' ', 1)[0] + '...'
    else:
        summary = row['title'][:150]
    
    summaries.append(summary)

df['summary'] = summaries

# Reorder
column_order = ['title', 'summary', 'content_text', 'link', 'time', 'category', 'source', 'site']
df = df[column_order]

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

# Stats
with_content = df[df['content_text'].str.len() > 100]
print(f'\n✅ Complete in {elapsed/60:.1f} minutes')
print(f'   Success: {len(with_content)}/{len(df)} ({len(with_content)*100/len(df):.1f}%)')

# Samples
print(f'\n📝 Sample articles:\n')
for idx, row in with_content.head(2).iterrows():
    print(f'{idx+1}. {row["title"][:60]}...')
    print(f'   Content: {row["content_text"][:100]}...\n')

print(f'✅ Saved: data_cafe_enriched.csv & .json')
