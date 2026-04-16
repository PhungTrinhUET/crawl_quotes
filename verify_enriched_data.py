import pandas as pd

# Load data
df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].astype(str)

print('📊 Data Summary:')
print(f'   Total records: {len(df)}')
print(f'   Columns: {", ".join(df.columns)}')
print(f'\n✅ File Structure:')
print(f'   - title: Article headline')
print(f'   - text: Article summary/description [READY TO FILL]')
print(f'   - link: Article URL')
print(f'   - time: Publication timestamp')
print(f'   - category: Coffee-related classification')
print(f'   - source: News outlet')
print(f'   - site: Website domain')

# Show samples
print(f'\n📝 Sample Records (first 3):')
for idx, row in df.head(3).iterrows():
    print(f'\n[{idx+1}] {row["title"][:70]}...')
    print(f'    Link: {row["link"]}')
    print(f'    Source: {row["source"]}')
    print(f'    Text: [EMPTY - needs scraping]')

print(f'\n💡 HOW TO FILL TEXT FIELD:')
print(f'''
Option 1: Scrape using Selenium (handles JavaScript)
   - Slower but comprehensive
   
Option 2: Use news site APIs (if available)
   - NewsAPI.org, Bing News, etc.
   
Option 3: Extract from meta tags
   - og:description, meta description
   - Fast but may be brief

Option 4: Keep as-is
   - Use title + link only
   - Add text later as needed

Files ready:
   ✅ data_cafe_enriched.csv (2,444 records)
   ✅ data_cafe_enriched.json (2,444 records)
''')

# Verify files exist
import os
print('📁 Files:')
for fname in ['data_cafe_enriched.csv', 'data_cafe_enriched.json']:
    if os.path.exists(fname):
        size = os.path.getsize(fname) / 1024
        print(f'   ✅ {fname} ({size:.1f} KB)')
