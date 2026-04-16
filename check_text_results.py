import pandas as pd
import json

# Check scraping results
df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].astype(str)

# Count articles with text
with_text = df[df['text'].str.len() > 0]
print(f'✅ Articles with text: {len(with_text)}/{len(df)}')

# Show sample
if len(with_text) > 0:
    sample = with_text.iloc[0]
    print(f'\n📝 Sample article:')
    print(f'  Title:  {sample["title"][:65]}...')
    print(f'  Text:   {sample["text"][:100]}...')
    print(f'  Source: {sample["source"]}')
    print(f'  Link:   {sample["link"]}')
else:
    print(f'\n⚠️  No text scraped yet. Articles may need more parsing.')

# Update JSON file
json_data = df.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
print(f'\n✅ JSON file updated: data_cafe_enriched.json')
