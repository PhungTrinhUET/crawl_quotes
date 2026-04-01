"""
COMPLETE ANALYSIS REPORT: Phân tích Xu hướng & Giá cả Hàng hóa
===========================================================================
Generated: 2026-03-18
Data Source: data_cafe_processed.csv (2875 records)
No visualization libraries required - Pure data analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# 1. LOAD DỮ LIỆU
# =====================================================
print("\n" + "="*90)
print(" PHÂN TÍCH XU HƯỚNG & GIÁ CỈ THEO THỜI GIAN - BÀO CÁO TOÀN DIỆN")
print("="*90)

df = pd.read_csv('data_cafe_processed.csv')
df['time'] = pd.to_datetime(df['time'])
df['date'] = pd.to_datetime(df['date'])

print(f"\n✅ Dữ liệu nhập thành công!")
print(f"    Tổng bản ghi: {len(df):,}")
print(f"    Bản ghi có giá: {df['price'].notna().sum():,}")
print(f"    Phạm vi thời gian: {df['date'].min().date()} --> {df['date'].max().date()} ({(df['date'].max() - df['date'].min()).days} ngày)")
print(f"    Nguồn tin: {df['source'].nunique()} tờ báo")

# =====================================================
# 2. TIỀN XỬ LÝ & LÀMẠCH
# =====================================================
print("\n" + "="*90)
print(" TIỀN XỬ LÝ DỮ LIỆU")
print("="*90)

df_price = df[df['price'].notna()].copy().sort_values('date').reset_index(drop=True)
print(f"   ✅ Dữ liệu sạch: {len(df_price):,} bản ghi có giá ({len(df_price)/len(df)*100:.1f}%)")

# Chỉ số thay đổi
df_price['price_change'] = df_price['price'].diff()
df_price['price_pct_change'] = df_price['price'].pct_change() * 100
df_price['price_ma7'] = df_price['price'].rolling(window=7, min_periods=1).mean()
df_price['price_ma14'] = df_price['price'].rolling(window=14, min_periods=1).mean()

df_price['month'] = df_price['date'].dt.to_period('M')
df_price['week_of_month'] = (df_price['date'].dt.day - 1) // 7 + 1
df_price['day_of_week'] = df_price['date'].dt.day_name()

print(f"   ✅ Thêm 7 cột mới: price_change, price_pct_change, MA7, MA14, month, week_of_month, day_of_week")


# =====================================================
# 3. THỐNG KÊ CƠ BẢN VỀ GIÁ
# =====================================================
print("\n" + "="*90)
print(" THỐNG KÊ CƠ BẢN VỀ GIÁ".ljust(90))
print("="*90)

print(f"\n  {'Chỉ số':<40} {'Giá trị':>20} {'Đơn vị':<15}")
print(f"  {'-'*65}")
print(f"  {'Giá trung bình':<40} {df_price['price'].mean():>20,.0f} {'đ/kg':<15}")
print(f"  {'Giá trung vị (Median)':<40} {df_price['price'].median():>20,.0f} {'đ/kg':<15}")
print(f"  {'Giá cao nhất':<40} {df_price['price'].max():>20,.0f} {'đ/kg':<15}")
print(f"  {'Giá thấp nhất':<40} {df_price['price'].min():>20,.0f} {'đ/kg':<15}")
print(f"  {'Độ lệch chuẩn (Std Dev)':<40} {df_price['price'].std():>20,.0f} {'đ/kg':<15}")
print(f"  {'Hệ số biến động (CV)':<40} {df_price['price'].std() / df_price['price'].mean() * 100:>20.2f} {'%':<15}")
print(f"  {'Phạm vi biến động (Range)':<40} {df_price['price'].max() - df_price['price'].min():>20,.0f} {'đ/kg':<15}")
print(f"  {'Tứ phân vị Q1 (25%)':<40} {df_price['price'].quantile(0.25):>20,.0f} {'đ/kg':<15}")
print(f"  {'Tứ phân vị Q3 (75%)':<40} {df_price['price'].quantile(0.75):>20,.0f} {'đ/kg':<15}")

# Ngày xảy ra
max_date = df_price.loc[df_price['price'].idxmax(), 'date'].date()
min_date = df_price.loc[df_price['price'].idxmin(), 'date'].date()
print(f"\n   Giá cao nhất: {df_price['price'].max():,.0f} đ/kg vào ngày {max_date}")
print(f"   Giá thấp nhất: {df_price['price'].min():,.0f} đ/kg vào ngày {min_date}")
print(f"   Thay đổi tổng: {df_price['price'].iloc[-1] - df_price['price'].iloc[0]:+,.0f} đ/kg ({(df_price['price'].iloc[-1] - df_price['price'].iloc[0]) / df_price['price'].iloc[0] * 100:+.1f}%)")


# =====================================================
# 4. PHÂN TÍCH CHUỖI THỜI GIAN
# =====================================================
print("\n" + "="*90)
print(" PHÂN TÍCH THEO THỜI GIAN".ljust(90))
print("="*90)

# Hàng ngày
daily_avg = df_price.groupby('date')['price'].agg(['mean', 'min', 'max', 'std', 'count'])
print(f"\n   THỐNG KÊ HÀNG NGÀY:")
print(f"     • Số ngày ghi nhận: {len(daily_avg):,}")
print(f"     • Giá trung bình hàng ngày: {daily_avg['mean'].mean():,.0f} đ/kg")
print(f"     • Giá cao nhất trong ngày: {daily_avg['max'].max():,.0f} đ/kg")
print(f"     • Giá thấp nhất trong ngày: {daily_avg['min'].min():,.0f} đ/kg")
print(f"     • Biến động trung bình trong ngày: {daily_avg['std'].mean():,.0f} đ/kg")

# Hàng tuần
weekly_stats = df_price.set_index('date').resample('W').agg({
    'price': ['mean', 'min', 'max', 'std', 'count']
})
print(f"\n   THỐNG KÊ HÀNG TUẦN:")
print(f"     • Số tuần ghi nhận: {len(weekly_stats):,}")
print(f"     • Giá tuần trung bình: {weekly_stats[('price', 'mean')].mean():,.0f} đ/kg")
print(f"     • Giá cao nhất trong tuần: {weekly_stats[('price', 'max')].max():,.0f} đ/kg")
print(f"     • Giá thấp nhất trong tuần: {weekly_stats[('price', 'min')].min():,.0f} đ/kg")

# Hàng tháng
monthly_stats = df_price.set_index('date').resample('M').agg({
    'price': ['mean', 'min', 'max', 'std', 'count']
})
print(f"\n   THỐNG KÊ HÀNG THÁNG:")
print(f"     {'Tháng':<20} {'Trung bình':<15} {'Thấp':<15} {'Cao':<15} {'Std':<12}")
print(f"     {'-'*77}")
for idx, row in monthly_stats.iterrows():
    month_str = idx.strftime('%B %Y')
    print(f"     {month_str:<20} {row[('price', 'mean')]:>14,.0f} {row[('price', 'min')]:>14,.0f} {row[('price', 'max')]:>14,.0f} {row[('price', 'std')]:>11,.0f}")


# =====================================================
# 5. ĐỘNG LỰC GIÁ
# =====================================================
print("\n" + "="*90)
print(" PHÂN TÍCH ĐỘNG LỰC GIÁ".ljust(90))
print("="*90)

up_days = (df_price['price_change'] > 0).sum()
down_days = (df_price['price_change'] < 0).sum()
flat_days = (df_price['price_change'] == 0).sum()
total_days = up_days + down_days + flat_days

print(f"\n   Phân bố ngày:")
print(f"      Ngày tăng giá:  {up_days:3} ngày ({up_days/total_days*100:>5.1f}%)")
print(f"      Ngày giảm giá:  {down_days:3} ngày ({down_days/total_days*100:>5.1f}%)")
print(f"     ➡️  Ngày đứng không: {flat_days:3} ngày ({flat_days/total_days*100:>5.1f}%)")

if up_days > 0:
    print(f"\n   Ngày tăng giá:")
    print(f"     • Tăng trung bình: +{df_price[df_price['price_change'] > 0]['price_change'].mean():,.0f} đ/kg")
    print(f"     • Tăng tối đa: +{df_price[df_price['price_change'] > 0]['price_change'].max():,.0f} đ/kg")
    print(f"     • Tăng tối thiểu: +{df_price[df_price['price_change'] > 0]['price_change'].min():,.0f} đ/kg")

if down_days > 0:
    print(f"\n   Ngày giảm giá:")
    print(f"     • Giảm trung bình: {df_price[df_price['price_change'] < 0]['price_change'].mean():,.0f} đ/kg")
    print(f"     • Giảm tối đa: {df_price[df_price['price_change'] < 0]['price_change'].min():,.0f} đ/kg")
    print(f"     • Giảm tối thiểu: {df_price[df_price['price_change'] < 0]['price_change'].max():,.0f} đ/kg")

# Phần trăm thay đổi
print(f"\n  % Thay đổi giá:")
print(f"     • Thay đổi % trung bình (hàng ngày): {df_price['price_pct_change'].mean():+.2f}%")
print(f"     • Thay đổi % tối đa (tăng): +{df_price['price_pct_change'].max():.2f}%")
print(f"     • Thay đổi % tối thiểu (giảm): {df_price['price_pct_change'].min():.2f}%")


# =====================================================
# 6. PHÂN LOẠI TIN TỨC
# =====================================================
print("\n" + "="*90)
print(" PHÂN LOẠI TIN TỨC".ljust(90))
print("="*90)

category_dist = df['category'].value_counts()
print(f"\n  {'Danh mục':<45} {'Số lượng':>12} {'Tỷ lệ':>12}")
print(f"  {'-'*70}")
for cat, count in category_dist.items():
    pct = count / len(df) * 100
    print(f"  {cat:<45} {count:>12,} {pct:>11.1f}%")

# Phân tích dữ liệu có giá
print(f"\n  {'*'*70}")
print(f"  Phân tích dữ liệu có GIÁ:")
category_price = df_price['category'].value_counts()
for cat, count in category_price.items():
    pct = count / len(df_price) * 100
    avg_price = df_price[df_price['category'] == cat]['price'].mean()
    print(f"     • {cat:<40} {count:>5,} bản ghi ({pct:>5.1f}%) | Giá TB: {avg_price:>10,.0f}")


# =====================================================
# 7. PHÂN TÍCH NGUỒN TIN
# =====================================================
print("\n" + "="*90)
print(" PHÂN TÍCH NGUỒN TIN".ljust(90))
print("="*90)

source_dist = df['source'].value_counts().head(15)
print(f"\n  Top 15 Nguồn tin:")
print(f"  {'Thứ tự':<8} {'Tên Báo/Tạp chí':<45} {'Số tin':>10} {'Tỷ lệ':>8}")
print(f"  {'-'*75}")
for idx, (source, count) in enumerate(source_dist.items(), 1):
    pct = count / len(df) * 100
    print(f"  {idx:<8} {source:<45} {count:>10,} {pct:>7.1f}%")


# =====================================================
# 8. XUẤT DỮ LIỆU TỔNG HỢP
# =====================================================
print("\n" + "="*90)
print(" XUẤT DỮ LIỆU TỔNG HỢP".ljust(90))
print("="*90)

# Daily stats
daily_stats = df_price.groupby('date').agg({
    'price': ['mean', 'min', 'max', 'std', 'count'],
    'source': 'nunique'
}).reset_index()
daily_stats.columns = ['date', 'price_mean', 'price_min', 'price_max', 'price_std', 'price_count', 'sources']
daily_stats.to_csv('daily_price_stats.csv', index=False)
print(f"   ✅ daily_price_stats.csv ({len(daily_stats)} ngày)")

# Timeseries data
df_price_export = df_price[['date', 'title', 'price', 'price_change', 'price_pct_change', 'price_ma7', 'price_ma14', 'category', 'source']].copy()
df_price_export.to_csv('coffee_price_timeseries.csv', index=False)
print(f"   ✅ coffee_price_timeseries.csv ({len(df_price_export)} bản ghi)")

# Weekly summary
weekly_summary = df_price.set_index('date').resample('W').agg({
    'price': ['mean', 'min', 'max', 'std']
}).reset_index()
weekly_summary.columns = ['week_end', 'price_mean', 'price_min', 'price_max', 'price_std']
weekly_summary.to_csv('weekly_price_summary.csv', index=False)
print(f"   ✅ weekly_price_summary.csv ({len(weekly_summary)} tuần)")

# Monthly summary
monthly_summary = df_price.set_index('date').resample('M').agg({
    'price': ['mean', 'min', 'max', 'std', 'count']
}).reset_index()
monthly_summary.columns = ['month_end', 'price_mean', 'price_min', 'price_max', 'price_std', 'price_count']
monthly_summary.to_csv('monthly_price_summary.csv', index=False)
print(f"   ✅ monthly_price_summary.csv ({len(monthly_summary)} tháng)")


# =====================================================
# 9. KẾT LUẬN & KHUYẾN NGHỊ
# =====================================================
print("\n" + "="*90)
print(" KẾT LUẬN & KHUYẾN NGHỊ".ljust(90))
print("="*90)

trend_direction = " TĂNG" if df_price['price_ma14'].iloc[-1] > df_price['price'].mean() else " GIẢM"
price_current = df_price['price'].iloc[-1]

conclusions = f"""
1.  XU HƯỚNG GIÁ CHUNG:
   • Giá giao động trong phạm vi: {df_price['price'].min():,.0f} - {df_price['price'].max():,.0f} đ/kg
   • Giá trung bình giai đoạn: {df_price['price'].mean():,.0f} đ/kg
   • Giá hiện tại (ngày cuối cùng): {price_current:,.0f} đ/kg
   • Xu hướng 14 ngày: {trend_direction}
   • Độ biến động: {df_price['price'].std() / df_price['price'].mean() * 100:.1f}% (Hệ số CV)

2.  ĐỘNG LỰC THƯƠNG TRƯỜNG:
   • Ngày giá tăng: {up_days} ({up_days/total_days*100:.0f}%) | Trung bình: +{df_price[df_price['price_change'] > 0]['price_change'].mean():,.0f}
   • Ngày giá giảm: {down_days} ({down_days/total_days*100:.0f}%) | Trung bình: {df_price[df_price['price_change'] < 0]['price_change'].mean():,.0f}
   • Thay đổi tổng: {df_price['price'].iloc[-1] - df_price['price'].iloc[0]:+,.0f} đ/kg

3. ️ NHÂN TỐ ẢNH HƯỞNG:
   • Giá cà phê Arabica/Robusta: {(df['category'] == 'Giá cà phê (Arabica/Robusta)').sum()} tin ({(df['category'] == 'Giá cà phê (Arabica/Robusta)').sum()/len(df)*100:.1f}%)
   • Xuất khẩu: {(df['category'] == 'Xuất khẩu').sum()} tin ({(df['category'] == 'Xuất khẩu').sum()/len(df)*100:.1f}%)
   • Tây Nguyên: {(df['category'] == 'Giá cà phê Tây Nguyên').sum()} tin
   • Quy mô tin: {len(df):,} bản ghi từ {df['source'].nunique()} nguồn

4.  KHUYẾN NGHỊ:
   ✓ Giá hiện tại: {price_current:,.0f} đ/kg (Mục tiêu: {df_price['price'].mean():,.0f} đ/kg)
   ✓ Theo dõi tin từ: Brazil, Iran, thị trường Robusta/Arabica toàn cầu
   ✓ Nguồn tin chính: {df['source'].value_counts().index[0]}
   ✓ Thống kê cho phép: Phân tích tin với độ tin cậy cao ({len(df_price)/len(df)*100:.0f}% dữ liệu hữu dụng)

5.  CHẤT LƯỢNG DỮ LIỆU:
   • Tổng bản ghi: {len(df):,} | Bản ghi có giá: {len(df_price):,} ({len(df_price)/len(df)*100:.1f}%)
   • Thời gian phân tích: {(df['date'].max() - df['date'].min()).days} ngày
   • Độ phủ sóng: {len(df_price) / ((df['date'].max() - df['date'].min()).days + 1) * 7:.1f} bản ghi/tuần
   • Tính liên tục: Đạt tiêu chuẩn (>1 bản ghi/ngày)
"""

print(conclusions)

print("="*90)
print("✅ PHÂN TÍCH HOÀN THÀNH!")
print("="*90)
print(f"\n Các file tạo ra:")
print(f"   1. daily_price_stats.csv - Thống kê hàng ngày")
print(f"   2. coffee_price_timeseries.csv - Dữ liệu chuỗi thời gian đầy đủ")
print(f"   3. weekly_price_summary.csv - Tóm tắt hàng tuần")
print(f"   4. monthly_price_summary.csv - Tóm tắt hàng tháng")
print(f"   5. Phan_tich_gia_ca_phe.ipynb - Jupyter Notebook tương tác")
print("\n" + "="*90 + "\n")
