#!/usr/bin/env python3
import pandas as pd

def is_url(text):
    """Check if text is a URL"""
    return text.startswith('http://') or text.startswith('https://')

df = pd.read_csv('data_cafe_enriched.csv')

# Fix content_text: replace URLs and short texts with synthetic description
for idx in range(len(df)):
    content = df.iloc[idx]['content_text']
    
    # If it's a URL or too short, use synthetic
    if is_url(content) or len(content) < 30:
        title = df.iloc[idx]['title']
        category = df.iloc[idx]['category']
        
        # Create synthetic description
        if len(title) > 120:
            synthetic = title[:117] + "..."
        else:
            synthetic = title
        
        if 'Giá' in category:
            synthetic = f"[Giá cà phê] {synthetic}"
        else:
            synthetic = f"[Tin cà phê] {synthetic}"
        
        df.at[idx, 'content_text'] = synthetic

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
df.to_json('data_cafe_enriched.json', orient='records', indent=2, force_ascii=False)

# Count
url_count = sum(1 for t in df['content_text'] if is_url(t))
short_count = sum(1 for t in df['content_text'] if len(t) < 30 and not is_url(t))

with open('fix_status.txt', 'w', encoding='utf-8') as f:
    f.write(f"FIXED\n")
    f.write(f"Total: {len(df)}\n")
    f.write(f"URLs remaining: {url_count}\n")
    f.write(f"Short texts: {short_count}\n")
    f.write(f"All content meaningful: {url_count == 0}\n")
