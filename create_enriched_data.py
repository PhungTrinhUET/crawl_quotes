import pandas as pd
import json

# Load raw data with links
df = pd.read_csv('data_cafe.csv')

# Load processed data to get category mapping
df_cat = pd.read_csv('data_cafe_processed.csv')
category_map = dict(zip(df_cat['title'], df_cat['category']))

# Apply categories to raw data
df['category'] = df['title'].map(category_map)

# Filter only coffee-related articles
coffee_categories = ['Tin về cà phê', 'Giá cà phê (Arabica/Robusta)']
df_coffee = df[df['category'].isin(coffee_categories)].copy()

# Prepare final dataframe with enriched columns
df_final = df_coffee[['title', 'link', 'time', 'category', 'source', 'site']].copy()

# Add empty text field (to be filled later by crawling article content)
df_final['text'] = ''

# Reorder columns
column_order = ['title', 'text', 'link', 'time', 'category', 'source', 'site']
df_final = df_final[column_order]

# Save enriched CSV
df_final.to_csv('data_cafe_enriched.csv', index=False, encoding='utf-8')
print(f'✅ CSV created: data_cafe_enriched.csv')
print(f'   Records: {len(df_final)}')
print(f'   Columns: {df_final.columns.tolist()}')

# Save as JSON
json_data = df_final.to_json(orient='records', indent=2, force_ascii=False)
with open('data_cafe_enriched.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
print(f'\n✅ JSON created: data_cafe_enriched.json')
print(f'   File size: {len(json_data) / 1024:.2f} KB')

# Show sample
print('\n📋 Sample records (first 3):\n')
for idx, row in df_final.head(3).iterrows():
    print(f'{idx+1}. Title: {row["title"][:70]}...')
    print(f'   Link:  {row["link"]}')
    print(f'   Category: {row["category"]}')
    print(f'   Source: {row["source"]}\n')
