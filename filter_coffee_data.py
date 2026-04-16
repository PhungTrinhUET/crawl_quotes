import pandas as pd

df = pd.read_csv('data_cafe_processed.csv')
print(f'📊 Total rows: {len(df)}')
print(f'\n📈 Category distribution:')
print(df['category'].value_counts())

# Filter only coffee-related articles
coffee_categories = ['Tin về cà phê', 'Giá cà phê (Arabica/Robusta)']
df_coffee = df[df['category'].isin(coffee_categories)]

print(f'\n✅ Cleaned data: {len(df_coffee)} rows')

# Save cleaned file
df_coffee.to_csv('data_cafe_cleaned.csv', index=False, encoding='utf-8')
print('💾 Saved to: data_cafe_cleaned.csv')

print('\n📝 Sample (5 articles):')
for idx, (_, row) in enumerate(df_coffee[['title', 'category']].head(5).iterrows(), 1):
    title = row['title'][:65]
    print(f'{idx}. {title}... ({row["category"]})')
