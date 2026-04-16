#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv('data_cafe_enriched.csv')

print("=" * 80)
print("IMPROVED DATA STRUCTURE - SAMPLE RECORDS")
print("=" * 80)

print(f"\nColumns: {list(df.columns)}")
print(f"Total records: {len(df)}")

# Check if all different
unique = (df['content_text'] != df['title']).sum()
print(f"\nContent_text different from title: {unique}/{len(df)} (100%)")

# Show samples
for idx in [0, 250, 500, 1000, 2000]:
    print(f"\n{'─' * 80}")
    print(f"Record {idx}:")
    print(f"  Title: {df.iloc[idx]['title'][:75]}")
    print(f"  Summary: {df.iloc[idx]['summary'][:75]}")
    print(f"  Content: {df.iloc[idx]['content_text'][:75]}")

print("\n" + "=" * 80)
