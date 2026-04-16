import pandas as pd

df = pd.read_csv('data_cafe_enriched.csv')

# Find records where content_text differs from title
diff_records = df[df['content_text'] != df['title']]
print(f"Records with different content_text: {len(diff_records)}")
print()

if len(diff_records) > 0:
    print("First 5 samples with different content:")
    for i, idx in enumerate(diff_records.head(5).index):
        print(f"\nRecord {idx}:")
        print(f"  Title: {df.loc[idx, 'title'][:70]}...")
        print(f"  Summary: {df.loc[idx, 'summary'][:70]}...")
        print(f"  Content_text: {df.loc[idx, 'content_text'][:100]}...")
else:
    print("ERROR: No records with different content_text!")
    print("\nChecking first record:")
    print(f"  Title: {df.iloc[0]['title'][:70]}...")
    print(f"  Content_text: {df.iloc[0]['content_text'][:100]}...")
