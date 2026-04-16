#!/usr/bin/env python3
"""
Improve text fields to be distinct:
- title: original headline (unchanged)
- summary: shortened title (150 chars max)
- content_text: extract from meta tags (og:description, meta description, article subtitle)
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

df = pd.read_csv('data_cafe_enriched.csv')

def extract_description(url):
    """Extract meaningful description from meta tags"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=5, headers=headers, verify=False)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strategy 1: og:description (most reliable)
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            text = og_desc['content'].strip()
            if len(text) > 20:
                return text
        
        # Strategy 2: meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            text = meta_desc['content'].strip()
            if len(text) > 20:
                return text
        
        # Strategy 3: article subtitle/lead (common in news sites)
        subtitle = soup.find(['h2', 'p'], class_=['subtitle', 'lead', 'article-lead', 'article-description'])
        if subtitle:
            text = subtitle.get_text(strip=True)
            if len(text) > 20 and len(text) < 500:
                return text
        
        # Strategy 4: First p tag in article container
        article = soup.find(['article', 'div'], class_=['article-content', 'story-body', 'article-body'])
        if article:
            p = article.find('p')
            if p:
                text = p.get_text(strip=True)
                if len(text) > 20 and len(text) < 500:
                    return text
        
        return None
        
    except Exception as e:
        return None

print("=" * 70)
print("IMPROVING TEXT FIELDS")
print("=" * 70)
print(f"\nProcessing {len(df)} articles...")

# Extraction with progress tracking
results = {'success': 0, 'partial': 0, 'failed': 0}

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(extract_description, url): idx 
               for idx, url in enumerate(df['link'])}
    
    for i, future in enumerate(as_completed(futures)):
        idx = futures[future]
        try:
            content = future.result()
            if content:
                df.loc[idx, 'content_text'] = content
                results['success'] += 1
            else:
                results['partial'] += 1
        except Exception as e:
            results['failed'] += 1
        
        if (i + 1) % 200 == 0:
            print(f"  [{i+1}/{len(df)}] Success: {results['success']}, "
                  f"Partial: {results['partial']}, Failed: {results['failed']}")

# Create proper summary (shortened title with ellipsis)
df['summary'] = df['title'].apply(lambda x: x[:147] + '...' if len(str(x)) > 150 else str(x))

print(f"\n✓ Extraction Complete:")
print(f"  - Success: {results['success']} ({results['success']*100//len(df)}%)")
print(f"  - Partial/Fallback: {results['partial']}")
print(f"  - Failed: {results['failed']}")

# Show samples of different cases
print(f"\n✓ Sample Results:")
sample_idx = df[df['content_text'] != df['title']].head(3).index
for idx in sample_idx:
    print(f"\n  Record {idx}:")
    print(f"    Title: {df.loc[idx, 'title'][:60]}...")
    print(f"    Summary: {df.loc[idx, 'summary'][:60]}...")
    print(f"    Content: {df.loc[idx, 'content_text'][:80]}...")

# Save improved data
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
df.to_json('data_cafe_enriched.json', orient='records', force_ascii=False, indent=2)

print(f"\n" + "=" * 70)
print("✓ UPDATED FILES:")
print(f"  - data_cafe_enriched.csv")
print(f"  - data_cafe_enriched.json")
print("=" * 70)
