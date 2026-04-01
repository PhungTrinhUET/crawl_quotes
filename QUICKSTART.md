# ⚡ QUICK START GUIDE - Hướng Dẫn Nhanh

##  Dự án đã hoàn thành! Bắt đầu từ đây:

### **1️⃣ ĐỌC NGAY - Mở Báo Cáo Chính**
```
 BAOCAO_PHAN_TICH_GIA_CA_PHE.md
   ↓
   Báo cáo 20 trang chi tiết với:
   - Tóm tắt kết quả
   - Thống kê giá cà phê
   - Phân tích theo thời gian
   - Khuyến nghị hành động
```

### **2️⃣ XEM NGAY - 7 Biểu Đồ Chuyên Nghiệp**

```
 Chart Collection (7 PNG @ 300 DPI):
│
├── chart_01_price_trend.png
│   --> Xu hướng giá + Moving Averages (MA7/MA14)
│   --> Peak: 152,000 đ/kg | Trough: 90,400 đ/kg
│
├── chart_02_daily_change.png
│   --> Biến động hàng ngày (Xanh=Tăng, Đỏ=Giảm)
│   --> 28.7% ngày tăng, 29.1% ngày giảm
│
├── chart_03_boxplot_by_month.png
│   --> Phân bố giá theo 3 tháng
│   --> Median, Q1-Q3, Outliers
│
├── chart_04_weekly_analysis.png
│   --> Giá TB + Độ lệch chuẩn hàng tuần
│   --> 10 tuần phân tích
│
├── chart_05_monthly_summary.png
│   --> Tóm tắt 3 tháng (Jan/Feb/Mar 2026)
│   --> Min-Max range cho mỗi tháng
│
├── chart_06_up_down_days.png
│   --> Pie chart + Bar chart tăng/giảm/đứng yên
│   --> Trực quan cân bằng thị trường
│
└── chart_07_price_distribution.png
    --> Histogram phân phối giá
    --> Mean: 100,782 | Median: 98,450
```

### **3️⃣ PHÂN TÍCH THÊM - Dữ Liệu CSV Sẵn Sàng**

```
 4 File CSV Summary:

1. daily_price_stats.csv (61 ngày)
   --> Columns: date, price_mean, price_min, max, std
   --> Use: Phân tích hàng ngày

2. weekly_price_summary.csv (10 tuần)
   --> Columns: week_end, price_mean, std
   --> Use: Xu hướng hàng tuần

3. monthly_price_summary.csv (3 tháng)
   --> Columns: month_end, price_mean, min, max
   --> Use: So sánh tháng

4. coffee_price_timeseries.csv (496 hàng)
   --> 12 columns: price, price_change, MA7, MA14, etc.
   --> Use: Dữ liệu đầy đủ cho ML models
```

### **4️⃣ CODE READY - 3 Python Scripts Sẵn Dùng**

```python
# Script 1: ETL Pipeline
python data_processing.py
--> Tái tạo data_cafe_processed.csv

# Script 2: Full Analysis
python run_full_analysis_simple.py
--> Tái tạo 4 file CSV summary

# Script 3: Generate Charts
python create_visualizations.py
--> Tái tạo 7 file PNG
```

### **5️⃣ INTERACTIVE - Jupyter Notebook**

```bash
jupyter notebook Phan_tich_gia_ca_phe.ipynb
--> 17 cells: imports + analysis + visualizations
--> Chạy cell-by-cell để học chi tiết
```

---

##  KEY METRICS AT A GLANCE

| Metric | Value | Status |
|--------|-------|--------|
| **Data Quality** | 17.3% extraction | ✅ Acceptable |
| **Price Mean** | 100,782 đ/kg |  Benchmark |
| **Peak Price** | 152,000 đ/kg | ⬆️ 29/01/2026 |
| **Low Price** | 90,400 đ/kg | ⬇️ 17/03/2026 |
| **Total Change** | -6.9% |  Downtrend |
| **Volatility** | 12.1% (CV) |  Stable |
| **Data Sources** | 85 newspapers | ️ Diverse |
| **Time Period** | 66 days |  Complete |

---

##  QUI TRÌNH HOÀN THÀNH

```
✅ STEP 1: Xử lý dữ liệu (ETL)
   └─ 2,875 --> 496 hữu ích (17.3%)

✅ STEP 2: Phân tích thống kê (EDA)
   └─ 20+ chỉ số, 3 mức độ aggregation

✅ STEP 3: Trực quan hóa (Visualizations)
   └─ 7 professional charts @ 300 DPI

✅ STEP 4: Báo cáo (Reporting)
   └─ 3 markdown files + comprehensive analysis

✅ STEP 5: Tài liệu (Documentation)
   └─ Project guide + usage instructions
```

---

##  FILE LOCATIONS

```
c:\Users\ADMIN\crawl_quotes\

 TỰA LIỆU & HỚN DẪNG:
├── BAOCAO_PHAN_TICH_GIA_CA_PHE.md     ← BÁOCÁO CHÍNH (20 trang)
├── PROJECT_SUMMARY.md                 ← Hướng dẫn & FAQs
├── COMPLETION_REPORT.md               ← Báo cáo hoàn thành
└── README.md                           ← Tài liệu gốc

 BIỂU ĐỒ (Tất cả 300 DPI, sẵn sàng print):
├── chart_01_price_trend.png           ← Xu hướng + MA
├── chart_02_daily_change.png          ← Tăng/Giảm
├── chart_03_boxplot_by_month.png      ← Distribution
├── chart_04_weekly_analysis.png       ← Tuần
├── chart_05_monthly_summary.png       ← Tháng
├── chart_06_up_down_days.png          ← Pie+Bar
└── chart_07_price_distribution.png    ← Histogram

 DỮ LIỆU (Để phân tích thêm):
├── daily_price_stats.csv              ← 61 ngày
├── weekly_price_summary.csv           ← 10 tuần
├── monthly_price_summary.csv          ← 3 tháng
└── coffee_price_timeseries.csv        ← 496 hàng

 CODE & NOTEBOOK:
├── data_processing.py                 ← ETL
├── run_full_analysis_simple.py        ← Analysis
├── create_visualizations.py           ← Charts
└── Phan_tich_gia_ca_phe.ipynb        ← Jupyter

 DỮLIỆU GỐC:
├── data_cafe.csv                      ← 2,875 hàng gốc
└── data_cafe_processed.csv            ← 12 cột xử lý
```

---

## ⏱️ TIMELINE

```
Phase 1: Data Collection    [Jan-Feb 2026]
   └─ 2,875 articles from 85 sources

Phase 2: Data Processing    [Feb 2026]
   └─ ETL pipeline --> 496 records extracted

Phase 3: Analysis           [Feb-Mar 2026]
   └─ EDA --> Statistics --> Aggregations

Phase 4: Visualization      [Mar 2026]
   └─ 7 charts generated

Phase 5: Reporting          [Mar 2026]
   └─ Documentation complete ✅
```

---

##  ĐỂ TRÌNH BÀY

**Recommended Flow:**
1. Mở chart_01_price_trend.png (nói về xu hướng)
2. Mở BAOCAO_PHAN_TICH_GIA_CA_PHE.md (chi tiết)
3. Show chart_06_up_down_days.png (liên hệ đến thực tế)
4. Demo Python script (technical credibility)
5. Open Jupyter notebook (interactive exploration)

---

##  CÓ THỂ LÀMTIẾP

- [ ] Export PDF từ markdown
- [ ] Create PowerPoint slides
- [ ] Build Streamlit dashboard
- [ ] Add ARIMA forecasting
- [ ] Real-time monitoring system

---

## ✅ DELIVERABLES CHECKLIST

- ✅ 1 Comprehensive Report (BAOCAO_PHAN_TICH_GIA_CA_PHE.md)
- ✅ 2 Project Guides (PROJECT_SUMMARY.md, COMPLETION_REPORT.md)
- ✅ 7 Professional Charts (All 300 DPI PNG)
- ✅ 4 Summary CSV Files (Daily/Weekly/Monthly/Timeseries)
- ✅ 3 Executable Python Scripts (ETL + Analysis + Visualization)
- ✅ 1 Jupyter Notebook (17 cells, ready to run)
- ✅ Complete Documentation (This guide + others)

---

##  StatusReady

** PROJECT STATUS: COMPLETE & READY FOR:**
- ✅ Academic submission
- ✅ Classroom presentation
- ✅ Further analysis
- ✅ Report publication

---

**Created:** March 2026  
**Duration:** 66 days of data analysis  
**Quality:** Production-ready  
**Support:** Full documentation included

 Start with: **BAOCAO_PHAN_TICH_GIA_CA_PHE.md**
