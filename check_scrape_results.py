import pandas as pd

df = pd.read_csv('data_cafe_enriched.csv')
df['text'] = df['text'].astype(str)

# Count records with text
with_text = df[df['text'].str.len() > 0]
print(f'✅ Total records with text: {len(with_text)}/{len(df)} ({len(with_text)*100/len(df):.1f}%)')

# Show samples
print(f'\n📝 Sample articles:\n')
for idx, row in with_text.head(3).iterrows():
    text_len = len(row['text'])
    is_title = row['text'] == row['title']
    status = '(title)' if is_title else f'({text_len} chars)'
    print(f'{idx+1}. {row["title"][:60]}...')
    print(f'   Text: {row["text"][:80]}... {status}\n')
