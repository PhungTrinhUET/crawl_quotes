#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo biểu đồ visualizations cho phân tích giá cà phê
Coffee Price Analysis - Visualization Script
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Thiết lập font cho tiếng Việt
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# Tải dữ liệu
print(" Tạo biểu đồ phân tích giá cà phê...")
print("-" * 60)

df_ts = pd.read_csv('coffee_price_timeseries.csv')
df_ts['date'] = pd.to_datetime(df_ts['date'])

df_daily = pd.read_csv('daily_price_stats.csv')
df_daily['date'] = pd.to_datetime(df_daily['date'])

df_weekly = pd.read_csv('weekly_price_summary.csv')
df_weekly['week_end'] = pd.to_datetime(df_weekly['week_end'])

df_monthly = pd.read_csv('monthly_price_summary.csv')
df_monthly['month_end'] = pd.to_datetime(df_monthly['month_end'])

# ============================================================================
# Chart 1: Giá theo thời gian + Moving Averages
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))

# Vẽ đường giá
ax.plot(df_ts['date'], df_ts['price'], linewidth=1.5, color='#2E86AB', 
        label='Giá hàng ngày', alpha=0.7)

# Vẽ MA7 và MA14
ax.plot(df_ts['date'], df_ts['price_ma7'], linewidth=2, color='#A23B72', 
        label='Moving Average 7 ngày', alpha=0.8)
ax.plot(df_ts['date'], df_ts['price_ma14'], linewidth=2, color='#F18F01', 
        label='Moving Average 14 ngày', alpha=0.8)

# Đánh dấu max/min
max_idx = df_ts['price'].idxmax()
min_idx = df_ts['price'].idxmin()

ax.scatter(df_ts.loc[max_idx, 'date'], df_ts.loc[max_idx, 'price'], 
          color='green', s=200, zorder=5, edgecolors='darkgreen', linewidth=2,
          label=f"Cao nhất: 152,000 (29/01)")
ax.scatter(df_ts.loc[min_idx, 'date'], df_ts.loc[min_idx, 'price'], 
          color='red', s=200, zorder=5, edgecolors='darkred', linewidth=2,
          label=f"Thấp nhất: 90,400 (17/03)")

ax.set_xlabel('Ngày', fontsize=11, fontweight='bold')
ax.set_ylabel('Giá (đ/kg)', fontsize=11, fontweight='bold')
ax.set_title('Xu Hướng Giá Cà Phê - Phân Tích Theo Thời Gian\n(Từ 12/01 đến 18/03/2026)', 
            fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('chart_01_price_trend.png', dpi=300, bbox_inches='tight')
print("✅ chart_01_price_trend.png")
plt.close()

# ============================================================================
# Chart 2: Biến động hàng ngày (Daily Change Distribution)
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))

colors = ['#06A77D' if x >= 0 else '#D62828' for x in df_ts['price_change'].dropna()]
ax.bar(df_ts.dropna(subset=['price_change'])['date'], 
      df_ts.dropna(subset=['price_change'])['price_change'],
      color=colors, width=0.7, alpha=0.8, edgecolor='black', linewidth=0.5)

ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.axhline(y=df_ts['price_change'].mean(), color='orange', linestyle='--', 
          linewidth=2, label=f"Trung bình: {df_ts['price_change'].mean():.0f} đ/kg")

ax.set_xlabel('Ngày', fontsize=11, fontweight='bold')
ax.set_ylabel('Thay đổi giá (đ/kg)', fontsize=11, fontweight='bold')
ax.set_title('Biến Động Giá Hàng Ngày\n(Xanh = Tăng, Đỏ = Giảm)', 
            fontsize=13, fontweight='bold', pad=15)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('chart_02_daily_change.png', dpi=300, bbox_inches='tight')
print("✅ chart_02_daily_change.png")
plt.close()

# ============================================================================
# Chart 3: Biểu đồ hộp (Box plot) theo tháng
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

# Chuẩn bị dữ liệu
df_ts['month'] = df_ts['date'].dt.to_period('M')
months_data = [group['price'].dropna().values for name, group in df_ts.groupby('month')]
month_labels = [str(name) for name, group in df_ts.groupby('month')]

bp = ax.boxplot(months_data, labels=month_labels, patch_artist=True,
               notch=False, showmeans=True,
               meanprops=dict(marker='D', markerfacecolor='red', markersize=8))

for patch, color in zip(bp['boxes'], ['#FFD700', '#87CEEB', '#90EE90']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Tháng', fontsize=11, fontweight='bold')
ax.set_ylabel('Giá (đ/kg)', fontsize=11, fontweight='bold')
ax.set_title('Phân Bố Giá Cà Phê Theo Tháng\n(Hộp = Q1-Q3, Đường = Median, ◊ = Mean)', 
            fontsize=13, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig('chart_03_boxplot_by_month.png', dpi=300, bbox_inches='tight')
print("✅ chart_03_boxplot_by_month.png")
plt.close()

# ============================================================================
# Chart 4: Thống kê hàng tuần
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))

x_pos = np.arange(len(df_weekly))
width = 0.35

bars1 = ax.bar(x_pos - width/2, df_weekly['price_mean'], width, 
              label='Giá TB', color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=0.5)
ax2 = ax.twinx()
bars2 = ax2.plot(x_pos, df_weekly['price_std'], 'ro-', linewidth=2, markersize=8,
                label='Std Dev', color='#E63946')

ax.set_xlabel('Tuần kết thúc', fontsize=11, fontweight='bold')
ax.set_ylabel('Giá trung bình (đ/kg)', fontsize=11, fontweight='bold', color='#2E86AB')
ax2.set_ylabel('Độ lệch chuẩn (đ/kg)', fontsize=11, fontweight='bold', color='red')
ax.set_title('Phân Tích Giá Theo Tuần\n(Cột = Giá TB, Đường = Độ biến động)', 
            fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x_pos)
ax.set_xticklabels([d.strftime('%d/%m') for d in df_weekly['week_end']], rotation=45, ha='right')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')

# Thêm legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('chart_04_weekly_analysis.png', dpi=300, bbox_inches='tight')
print("✅ chart_04_weekly_analysis.png")
plt.close()

# ============================================================================
# Chart 5: Thống kê hàng tháng
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

months = [d.strftime('%b %Y') for d in df_monthly['month_end']]
colors_month = ['#FF6B6B', '#4ECDC4', '#45B7D1']

bars = ax.bar(months, df_monthly['price_mean'], color=colors_month, 
             alpha=0.8, edgecolor='black', linewidth=2, width=0.6)

# Thêm giá trị lên trên cột
for bar, val_mean, val_min, val_max in zip(bars, df_monthly['price_mean'], 
                                           df_monthly['price_min'], df_monthly['price_max']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
           f'{val_mean:,.0f}\n[{val_min:,.0f}-{val_max:,.0f}]',
           ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Giá (đ/kg)', fontsize=11, fontweight='bold')
ax.set_title('Thống Kê Giá Cà Phê Hàng Tháng\n(Giá TB [Min-Max])', 
            fontsize=13, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig('chart_05_monthly_summary.png', dpi=300, bbox_inches='tight')
print("✅ chart_05_monthly_summary.png")
plt.close()

# ============================================================================
# Chart 6: Phân bố tăng/giảm (Up vs Down days)
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
price_changes = df_ts['price_change'].dropna()
up_days = len(price_changes[price_changes > 0])
down_days = len(price_changes[price_changes < 0])
flat_days = len(price_changes[price_changes == 0])

sizes = [up_days, down_days, flat_days]
labels = [f'Ngày Tăng\n{up_days} ({up_days/len(price_changes)*100:.1f}%)',
         f'Ngày Giảm\n{down_days} ({down_days/len(price_changes)*100:.1f}%)',
         f'Ngày Đứng Yên\n{flat_days} ({flat_days/len(price_changes)*100:.1f}%)']
colors_pie = ['#06A77D', '#D62828', '#999999']
explode = (0.05, 0.05, 0)

ax1.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
       shadow=True, startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
ax1.set_title('Phân Bố Ngày Tăng/Giảm/Đứng Yên', fontsize=12, fontweight='bold', pad=10)

# Bar chart so sánh
categories = ['Tăng', 'Giảm', 'Đứng Yên']
values = [up_days, down_days, flat_days]
bars = ax2.bar(categories, values, color=colors_pie, alpha=0.8, 
              edgecolor='black', linewidth=1.5, width=0.6)

for bar, val in zip(bars, values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{val}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_ylabel('Số ngày', fontsize=11, fontweight='bold')
ax2.set_title('So Sánh Số Ngày Tăng/Giảm/Đứng Yên', fontsize=12, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')

plt.tight_layout()
plt.savefig('chart_06_up_down_days.png', dpi=300, bbox_inches='tight')
print("✅ chart_06_up_down_days.png")
plt.close()

# ============================================================================
# Chart 7: Phân phối giá (Histogram)
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))

prices = df_ts['price'].dropna()
ax.hist(prices, bins=30, color='#5E548E', alpha=0.7, edgecolor='black', linewidth=1)

ax.axvline(prices.mean(), color='red', linestyle='--', linewidth=2.5, 
          label=f'Trung bình: {prices.mean():.0f} đ/kg')
ax.axvline(prices.median(), color='green', linestyle='--', linewidth=2.5,
          label=f'Trung vị: {prices.median():.0f} đ/kg')

ax.set_xlabel('Giá (đ/kg)', fontsize=11, fontweight='bold')
ax.set_ylabel('Tần suất', fontsize=11, fontweight='bold')
ax.set_title('Phân Phối Giá Cà Phê\n(Histogram)', fontsize=13, fontweight='bold', pad=15)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig('chart_07_price_distribution.png', dpi=300, bbox_inches='tight')
print("✅ chart_07_price_distribution.png")
plt.close()

print("-" * 60)
print("✅ HOÀN THÀNH! Tất cả 7 biểu đồ đã được tạo:")
print()
print("  1. chart_01_price_trend.png - Xu hướng giá + Moving Averages")
print("  2. chart_02_daily_change.png - Biến động hàng ngày")
print("  3. chart_03_boxplot_by_month.png - Phân bố giá theo tháng")
print("  4. chart_04_weekly_analysis.png - Thống kê hàng tuần")
print("  5. chart_05_monthly_summary.png - Tóm tắt hàng tháng")
print("  6. chart_06_up_down_days.png - Tăng/Giảm/Đứng Yên")
print("  7. chart_07_price_distribution.png - Phân phối giá")
print()
print(" Các file có sẵn:")
print("  - BAOCAO_PHAN_TICH_GIA_CA_PHE.md (Báo cáo chi tiết)")
print("  - daily_price_stats.csv (Thống kê hàng ngày)")
print("  - weekly_price_summary.csv (Thống kê hàng tuần)")
print("  - monthly_price_summary.csv (Thống kê hàng tháng)")
print("  - coffee_price_timeseries.csv (Dữ liệu đầy đủ)")
print("=" * 60)
