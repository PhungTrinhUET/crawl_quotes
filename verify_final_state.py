#!/usr/bin/env python3
import pandas as pd
import json
import os

print("=" * 60)
print("FINAL DATA VERIFICATION")
print("=" * 60)

# Check CSV
csv_path = 'data_cafe_enriched.csv'
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print(f"\n✓ CSV File: {csv_path}")
    print(f"  - Records: {len(df)}")
    print(f"  - Columns: {list(df.columns)}")
    print(f"  - Size: {os.path.getsize(csv_path) / 1024:.1f} KB")
    
    # Sample
    print(f"\n  First record:")
    print(f"    Title: {df.iloc[0]['title'][:60]}...")
    print(f"    Link: {df.iloc[0]['link']}")
    print(f"    Category: {df.iloc[0]['category']}")
    print(f"    Source: {df.iloc[0]['source']}")
else:
    print(f"\n✗ CSV File not found: {csv_path}")

# Check JSON
json_path = 'data_cafe_enriched.json'
if os.path.exists(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            j = json.load(f)
        print(f"\n✓ JSON File: {json_path}")
        print(f"  - Records: {len(j)}")
        print(f"  - Size: {os.path.getsize(json_path) / 1024:.1f} KB")
    except Exception as e:
        print(f"\n⚠ JSON File exists but has encoding issue: {e}")
else:
    print(f"\n✗ JSON File not found: {json_path}")

# Source distribution
print(f"\n✓ Data Distribution by Source:")
source_counts = df['source'].value_counts().head(10)
for source, count in source_counts.items():
    print(f"  - {source}: {count} articles")

# Category distribution
print(f"\n✓ Data Distribution by Category:")
category_counts = df['category'].value_counts()
for cat, count in category_counts.items():
    print(f"  - {cat}: {count} articles")

print("\n" + "=" * 60)
print("DATA READY FOR ANALYSIS & EXPORT")
print("=" * 60)
