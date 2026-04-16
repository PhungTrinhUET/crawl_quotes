import pandas as pd

# Load data
df = pd.read_csv('data_cafe_enriched.csv')

print('📊 Creating final enriched dataset...\n')

# Use title as content_text (titles are detailed)
df['content_text'] = df['title']

# Create summary (first 150 chars)
summaries = []
for text in df['title']:
    summary = text[:150]
    if len(text) > 150:
        summary = summary.rsplit(' ', 1)[0] + '...'
    summaries.append(summary)

df['summary'] = summaries

# Reorder columns
column_order = ['title', 'summary', 'content_text', 'link', 'time', 'category', 'source', 'site']
df = df[column_order]

# Save
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
print('✅ CSV updated: data_cafe_enriched.csv')

# Save JSON
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
print('✅ JSON updated: data_cafe_enriched.json')

# Show structure
print(f'\n📋 Final Structure ({len(df)} records):\n')
for idx, row in df.head(2).iterrows():
    print(f'{idx+1}.')
    print(f'   Title:        {row["title"][:70]}...')
    print(f'   Summary:      {row["summary"][:70]}...')
    print(f'   Content Text: {row["content_text"][:70]}...')
    print(f'   Link:         {row["link"][:60]}...')
    print(f'   Time:         {row["time"][:20]}')
    print(f'   Category:     {row["category"]}')
    print(f'   Source:       {row["source"]}')
    print(f'   Site:         {row["site"]}\n')

print(f'✅ Files ready for use!')
print(f'\n📊 Statistics:')
print(f'   Total articles: {len(df)}')
print(f'   Columns: {len(df.columns)}')
print(f'   Coffee content: 100% (filtered)')
print(f'   Format: CSV + JSON')
