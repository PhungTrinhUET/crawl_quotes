import pandas as pd
import json

# Read cleaned CSV
df = pd.read_csv('data_cafe_cleaned.csv')

# Convert to JSON with proper formatting
json_data = df.to_json(orient='records', indent=2, force_ascii=False)

# Write to file
with open('data_cafe_cleaned.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print(f'✅ JSON file created: data_cafe_cleaned.json')
print(f'📊 Total records: {len(df)}')
print(f'📝 File size: {len(json_data) / 1024:.2f} KB')

# Show sample
print('\n📋 Sample (first 2 records):')
records = json.loads(json_data)
print(json.dumps(records[:2], indent=2, ensure_ascii=False))
