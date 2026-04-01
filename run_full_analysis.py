"""
FULL ANALYSIS REPORT: Phân tích Xu hướng & Giá cả Hàng hóa
===========================================================================
Generated: 2026-03-18
Data Source: data_cafe_processed.csv (2875 records)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =====================================================
# 1. LOAD & KHÁM PHÁ DỮ LIỆU
# =====================================================
print("\n" + "="*80)
print("📓 PHÂN TÍCH XU HƯỚNG & GIÁ CỈ THEO THỜI GIAN")
print("="*80)

df = pd.read_csv('data_cafe_processed.csv')
df['time'] = pd.to_datetime(df['time'])
df['date'] = pd.to_datetime(df['date'])

print(f"\n✅ Dữ liệu nhập thành công!")
print(f"📊 Tổng bản ghi: {len(df):,}")
print(f"📈 Bản ghi có giá: {df['price'].notna().sum():,}")
print(f"📅 Phạm vi thời gian: {df['date'].min().date()} → {df['date'].max().date()}")
print(f"📋 Cột dữ liệu: {', '.join(df.columns[:8])}...")


# =====================================================
# 2. TIỀN XỬ LÝ DỮ LIỆU
# =====================================================
print("\n" + "="*80)
print("🔧 TIỀN XỬ LÝ DỮ LIỆU")
print("="*80)

df_price = df[df['price'].notna()].copy().sort_values('date').reset_index(drop=True)

# Chỉ số thay đổi
df_price['price_change'] = df_price['price'].diff()
df_price['price_pct_change'] = df_price['price'].pct_change() * 100

# Moving averages
df_price['price_ma7'] = df_price['price'].rolling(window=7, min_periods=1).mean()
df_price['price_ma14'] = df_price['price'].rolling(window=14, min_periods=1).mean()

df_price['month'] = df_price['date'].dt.to_period('M')
df_price['week_of_month'] = (df_price['date'].dt.day - 1) // 7 + 1
df_price['day_of_week'] = df_price['date'].dt.day_name()

print(f"✅ Thêm cột: price_change, price_pct_change, MA7, MA14")
print(f"✅ Dữ liệu sạch: {len(df_price):,} bản ghi")


# =====================================================
# 3. THỐNG KÊ CƠ BẢN
# =====================================================
print("\n" + "="*80)
print("📊 THỐNG KÊ CƠ BẢN VỀ GIÁ")
print("="*80)

stats = {
    'Giá trung bình': df_price['price'].mean(),
    'Giá trung vị': df_price['price'].median(),
    'Giá cao nhất': df_price['price'].max(),
    'Giá thấp nhất': df_price['price'].min(),
    'Độ lệch chuẩn': df_price['price'].std(),
    'Hệ số biến động (CV)': df_price['price'].std() / df_price['price'].mean() * 100,
    'Phạm vi biến động': df_price['price'].max() - df_price['price'].min(),
}

for key, value in stats.items():
    if 'CV' in key or 'Hệ' in key:
        print(f"  {key:.<40} {value:.2f}%")
    else:
        print(f"  {key:.<40} {value:>12,.0f} đ/kg")

# Top insights
print(f"\n📌 Giá cao nhất: {df_price['price'].max():,.0f} đ/kg ({df_price.loc[df_price['price'].idxmax(), 'date'].date()})")
print(f"📌 Giá thấp nhất: {df_price['price'].min():,.0f} đ/kg ({df_price.loc[df_price['price'].idxmin(), 'date'].date()})")
print(f"📌 Thay đổi tổng: {df_price['price'].iloc[-1] - df_price['price'].iloc[0]:+,.0f} đ/kg")


# =====================================================
# 4. PHÂN TÍCH CHUỖI THỜI GIAN
# =====================================================
print("\n" + "="*80)
print("📈 PHÂN TÍCH THEO THỜI GIAN")
print("="*80)

# Hàng ngày
daily_avg = df_price.groupby('date')['price'].mean()
print(f"\n📅 THỐNG KÊ HÀNG NGÀY:")
print(f"  Số ngày ghi nhận: {len(daily_avg):,}")
print(f"  Giá hàng ngày trung bình: {daily_avg.mean():,.0f} đ/kg")
print(f"  Giá cao nhất trong ngày: {daily_avg.max():,.0f} đ/kg")
print(f"  Giá thấp nhất trong ngày: {daily_avg.min():,.0f} đ/kg")

# Hàng tuần
weekly_stats = df_price.set_index('date').resample('W').agg({
    'price': ['mean', 'min', 'max', 'std', 'count']
})
print(f"\n📊 THỐNG KÊ HÀNG TUẦN:")
print(f"  Số tuần ghi nhận: {len(weekly_stats):,}")
print(f"  Giá tuần trung bình: {weekly_stats[('price', 'mean')].mean():,.0f} đ/kg")

# Hàng tháng
monthly_stats = df_price.set_index('date').resample('M').agg({
    'price': ['mean', 'min', 'max', 'std', 'count']
})
print(f"\n📆 THỐNG KÊ HÀNG THÁNG:")
for idx, row in monthly_stats.iterrows():
    print(f"  {idx.strftime('%B %Y'):.<25} TB: {row[('price', 'mean')]:>8,.0f} | Min: {row[('price', 'min')]:>8,.0f} | Max: {row[('price', 'max')]:>8,.0f}")


# =====================================================
# 5. PHÂN TÍCH ĐỘNG LỰC GIÁ
# =====================================================
print("\n" + "="*80)
print("💹 PHÂN TÍCH ĐỘNG LỰC GIÁ")
print("="*80)

up_days = (df_price['price_change'] > 0).sum()
down_days = (df_price['price_change'] < 0).sum()
flat_days = (df_price['price_change'] == 0).sum()

print(f"\n📊 Ngày tăng giá: {up_days:3} ngày ({up_days/(up_days+down_days+flat_days)*100:>5.1f}%)")
print(f"📊 Ngày giảm giá: {down_days:3} ngày ({down_days/(up_days+down_days+flat_days)*100:>5.1f}%)")
print(f"📊 Ngày đứng không:  {flat_days:3} ngày ({flat_days/(up_days+down_days+flat_days)*100:>5.1f}%)")

if up_days > 0:
    print(f"\n💹 Ngày tăng giá:")
    print(f"  Tăng trung bình: +{df_price[df_price['price_change'] > 0]['price_change'].mean():,.0f} đ/kg")
    print(f"  Tăng tối đa: +{df_price[df_price['price_change'] > 0]['price_change'].max():,.0f} đ/kg")

if down_days > 0:
    print(f"\n📉 Ngày giảm giá:")
    print(f"  Giảm trung bình: {df_price[df_price['price_change'] < 0]['price_change'].mean():,.0f} đ/kg")
    print(f"  Giảm tối đa: {df_price[df_price['price_change'] < 0]['price_change'].min():,.0f} đ/kg")


# =====================================================
# 6. PHÂN TÍCH THEO TUẦN TRONG THÁNG
# =====================================================
print("\n" + "="*80)
print("📅 PHÂN TÍCH THEO TUẦN TRONG THÁNG")
print("="*80)

weekly_price = df_price.groupby('week_of_month')['price'].agg(['mean', 'std', 'count'])
for week in range(1, 6):
    if week in weekly_price.index:
        row = weekly_price.loc[week]
        print(f"\nTuần {week}: Giá TB = {row['mean']:>9,.0f} | Std Deviation = {row['std']:>8,.0f} | Số ngày = {int(row['count']):>2}")


# =====================================================
# 7. PHÂN TÍCH DANH MỤC TIN TỨC
# =====================================================
print("\n" + "="*80)
print("📋 PHÂN LOẠI TIN TỨC")
print("="*80)

category_dist = df['category'].value_counts()
for cat, count in category_dist.items():
    pct = count / len(df) * 100
    print(f"  {cat:.<45} {count:>5} ({pct:>5.1f}%)")


# =====================================================
# 8. TẢI DỮIỆU TỔNG HỢP
# =====================================================
print("\n" + "="*80)
print("💾 XUẤT DỮ LIỆU TỔNG HỢP")
print("="*80)

# Lưu daily stats
daily_stats = df_price.groupby('date').agg({
    'price': ['mean', 'min', 'max', 'std'],
    'source': 'nunique'
}).reset_index()
daily_stats.columns = ['date', 'price_mean', 'price_min', 'price_max', 'price_std', 'sources']
daily_stats.to_csv('daily_price_stats.csv', index=False)
print(f"✅ Lưu vào: daily_price_stats.csv ({len(daily_stats)} ngày)")

# Lưu price data đã xử lý
df_price.to_csv('coffee_price_timeseries.csv', index=False)
print(f"✅ Lưu vào: coffee_price_timeseries.csv ({len(df_price)} bản ghi)")


# =====================================================
# 9. KẾT LUẬN
# =====================================================
print("\n" + "="*80)
print("🎯 KẾT LUẬN & KHUYẾN NGHỊ")
print("="*80)

conclusion = f"""
1. 📊 XU HƯỚNG GIÁ CHUNG:
   • Giá giao động trong phạm vi {df_price['price'].min():,.0f} - {df_price['price'].max():,.0f} đ/kg
   • Giá trung bình: {df_price['price'].mean():,.0f} đ/kg
   • Độ biến động (CV): {df_price['price'].std() / df_price['price'].mean() * 100:.1f}%

2. 📈 ĐỘNG LỰC THƯƠNG TRƯỜNG:
   • Số ngày tăng giá: {up_days} ({up_days/(up_days+down_days)*100:.0f}%)
   • Số ngày giảm giá: {down_days} ({down_days/(up_days+down_days)*100:.0f}%)
   • Giá hiện tại: ~{df_price['price'].iloc[-1]:,.0f} đ/kg

3. 👁️ NHÂN TỐ ẢNH HƯỞNG:
   • Thị trường Robusta & Arabica: {(df['category'] == 'Giá cà phê (Arabica/Robusta)').sum()} tin
   • Xuất khẩu: {(df['category'] == 'Xuất khẩu').sum()} tin
   • Tây Nguyên: {(df['category'] == 'Giá cà phê Tây Nguyên').sum()} tin

4. 🔮 DỰ BÁO & KHUYẾN NGHỊ:
   • Giá có xu hướng {('tăng' if df_price['price_ma14'].iloc[-1] > df_price['price'].mean() else 'giảm')}
   • Nên theo dõi tin tức từ: Iran, Brazil, thị trường toàn cầu
   • Nguồn tin chính: {df['source'].value_counts().index[0]}

5. 📊 CHẤT LƯỢNG DỮ LIỆU:
   • Tổng tin: {len(df):,} | Có giá: {len(df_price):,} ({len(df_price)/len(df)*100:.1f}%)
   • Thời gian: {(df['date'].max() - df['date'].min()).days} ngày
   • Nguồn tin: {df['source'].nunique()} tờ báo
"""

print(conclusion)

print("\n" + "="*80)
print("✅ PHÂN TÍCH HOÀN THÀNH!")
print("="*80)
print(f"📁 Các file tạo ra:")
print(f"   • daily_price_stats.csv")
print(f"   • coffee_price_timeseries.csv")
print(f"   • Phan_tich_gia_ca_phe.ipynb (Jupyter Notebook)")
print("="*80 + "\n")
