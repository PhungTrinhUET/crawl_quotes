#!/usr/bin/env python3
"""
Improve data with better content extraction:
- Keep extracted metas that are actually useful (not URLs)
- Create meaningful summaries from title
- Fallback to structured title-based content for others
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data_cafe_enriched.csv')

def extract_proper_description(url):
    """Extract meaningful description, avoid URLs"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=5, headers=headers, verify=False)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try og:description and meta description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            text = og_desc['content'].strip()
            # Only keep if it's real text, not a URL
            if text and not text.startswith('http') and len(text) > 30 and len(text) < 500:
                return text
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            text = meta_desc['content'].strip()
            if text and not text.startswith('http') and len(text) > 30 and len(text) < 500:
                return text
        
        # Try article subtitle
        for tag in soup.find_all(['h2', 'p'], class_=True):
            classes = ' '.join(tag.get('class', []))
            if 'subtitle' in classes or 'lead' in classes or 'sapo' in classes:
                text = tag.get_text(strip=True)
                if text and not text.startswith('http') and len(text) > 30 and len(text) < 500:
                    return text
        
        return None
        
    except Exception:
        return None

print("=" * 70)
print("CREATING MEANINGFUL TEXT FIELDS")
print("=" * 70)

# Reset content_text to original titles first
df['content_text'] = df['title']
results = {'real_desc': 0, 'structured': 0}

# Re-extract with better validation
print("\nRe-extracting descriptions (avoiding URLs)...")
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(extract_proper_description, url): idx 
               for idx, url in enumerate(df['link'])}
    
    for i, future in enumerate(as_completed(futures)):
        idx = futures[future]
        try:
            content = future.result()
            if content:
                df.loc[idx, 'content_text'] = content
                results['real_desc'] += 1
        except:
            pass
        
        if (i + 1) % 500 == 0:
            print(f"  [{i+1}/2444] Real descriptions: {results['real_desc']}")

# For remaining records: create structured content from title + metadata
for idx, row in df.iterrows():
    if df.loc[idx, 'content_text'] == df.loc[idx, 'title']:
        # Create structured fallback from title + category + source
        category = row['category']
        source = row['source']
        title = row['title']
        
        # Build meaningful fallback
        if category == 'Giá cà phê (Arabica/Robusta)':
            fallback = f"Cập nhật giá cà phê: {title}. Nguồn: {source}"
        else:
            fallback = f"Tin về cà phê: {title}. Từ {source}."
        
        df.loc[idx, 'content_text'] = fallback
        results['structured'] += 1

# Create better summary: shortened title with ellipsis
def create_summary(title):
    """Create clean summary from title"""
    if len(title) <= 150:
        return title
    else:
        # Find safe break point before 150 chars
        safe_title = title[:147]
        last_space = safe_title.rfind(' ')
        if last_space > 100:
            return safe_title[:last_space] + '...'
        return safe_title + '...'

df['summary'] = df['title'].apply(create_summary)

print(f"\n✓ Processing Complete:")
print(f"  - Real descriptions extracted: {results['real_desc']}")
print(f"  - Structured fallback created: {results['structured']}")
print(f"  - Total: {len(df)}")

# Show samples
print(f"\n✓ Sample Results (diverse types):")
sample_indices = [0, 100, 500, 1000, 2000]
for idx in sample_indices:
    if idx < len(df):
        print(f"\nRecord {idx}:")
        print(f"  Title: {df.loc[idx, 'title'][:50]}...")
        print(f"  Summary: {df.loc[idx, 'summary'][:60]}...")
        print(f"  Content: {df.loc[idx, 'content_text'][:70]}...")

# Verify all three fields are distinct
distinct_pairs = (df['title'] != df['summary']).sum()
print(f"\n✓ Field Distinctness:")
print(f"  - Title != Summary: {distinct_pairs} records")

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
df.to_json('data_cafe_enriched.json', orient='records', force_ascii=False, indent=2)

print(f"\n" + "=" * 70)
print("✓ FILES UPDATED: CSV and JSON")
print("=" * 70)
