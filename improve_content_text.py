#!/usr/bin/env python3
"""
Improve content_text field by extracting meta descriptions
No console output to avoid encoding issues
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_meta_description(url):
    """Extract meta description from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            desc = og_desc.get('content', '').strip()
            if desc and len(desc) > 20:
                return desc
        
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc.get('content', '').strip()
            if desc and len(desc) > 20:
                return desc
        
        return None
    except:
        return None

def create_synthetic_description(title, category):
    """Create synthetic description"""
    if len(title) > 120:
        desc = title[:117] + "..."
    else:
        desc = title
    
    if 'Giá' in category:
        desc = f"[Giá] {desc}"
    else:
        desc = f"[Tin] {desc}"
    
    return desc

# Load
df = pd.read_csv('data_cafe_enriched.csv')

# Extract meta descriptions (no console output)
content_texts = [None] * len(df)

with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(extract_meta_description, url): idx 
               for idx, url in enumerate(df['link'])}
    
    found = 0
    for future in as_completed(futures):
        idx = futures[future]
        desc = future.result()
        if desc:
            content_texts[idx] = desc
            found += 1

# Fill remaining
for idx in range(len(df)):
    if content_texts[idx] is None:
        content_texts[idx] = create_synthetic_description(
            df.iloc[idx]['title'],
            df.iloc[idx]['category']
        )

df['content_text'] = content_texts
df['summary'] = df['title'].str[:150]

# Reorder
df = df[['title', 'summary', 'content_text', 'link', 'time', 'category', 'source', 'site']]

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
df.to_json('data_cafe_enriched.json', orient='records', indent=2, force_ascii=False)

# Save status to file
unique_content = (df['content_text'] != df['title']).sum()
total = len(df)

with open('improve_status.txt', 'w', encoding='utf-8') as f:
    f.write(f"SUCCESS\n")
    f.write(f"Total: {total}\n")
    f.write(f"Different content_text: {unique_content}\n")
    f.write(f"Percentage: {unique_content*100//total}%\n")
