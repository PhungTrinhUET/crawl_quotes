import pandas as pd

# Load enriched data
df = pd.read_csv('data_cafe_enriched.csv')

print(f'📥 Processing {len(df)} records...')

# Create summary and content_text columns
summaries = []
content_texts = []

for idx, row in df.iterrows():
    text = str(row['text'])
    
    # Summary: first 150 characters
    summary = text[:150]
    if len(text) > 150:
        summary = summary.rsplit(' ', 1)[0] + '...'
    
    # Content text: full text
    content_text = text
    
    summaries.append(summary)
    content_texts.append(content_text)
    
    if (idx + 1) % 500 == 0:
        print(f'  [{idx+1}/{len(df)}] processed')

# Add new columns
df['summary'] = summaries
df['content_text'] = content_texts

# Drop old text column
df = df.drop('text', axis=1)

# Reorder columns
column_order = ['title', 'summary', 'content_text', 'link', 'time', 'category', 'source', 'site']
df = df[column_order]

# Save CSV
df.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
print(f'\n✅ CSV updated: data_cafe_enriched.csv')

# Save JSON
json_str = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
print(f'✅ JSON updated: data_cafe_enriched.json')

# Show samples
print(f'\n📝 Sample structure:\n')
for idx, row in df.head(2).iterrows():
    print(f'{idx+1}. Title:        {row["title"][:60]}...')
    print(f'   Summary:      {row["summary"][:70]}...')
    print(f'   Content text: {row["content_text"][:70]}...')
    print(f'   Link:         {row["link"][:60]}...')
    print(f'   Category:     {row["category"]}')
    print()

print(f'✅ Columns: {", ".join(df.columns.tolist())}')
