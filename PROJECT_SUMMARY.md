#  DỰ ÁN PHÂN TÍCH XU HƯỚNG GIÁ CÀ PHÊ - WEB MINING PROJECT

**Tên Project:** Phân Tích Xu Hướng & Giá Cả Hàng Hóa Theo Thời Gian  
**Môn Học:** Khai Phá Dữ Liệu Web (Web Data Mining)  
**Ngày Hoàn Thành:** Tháng Ba 2026  
**Dữ Liệu Xử Lý:** 2,875 bản ghi --> 496 bản ghi hữu ích (17.3%)  
**Giai Đoạn Phân Tích:** 12/01/2026 - 18/03/2026 (66 ngày)

---

##  Nội Dung Dự Án

Dự án này thực hiện **quy trình khai phá dữ liệu web hoàn chỉnh** gồm:

1. ✅ **Thu Thập Dữ Liệu (Data Collection):** Scraping tin tức từ 85 tờ báo
2. ✅ **Xử Lý Dữ Liệu (Data Processing):** ETL pipeline để trích xuất giá từ tiêu đề tin
3. ✅ **Phân Tích Thống Kê (Statistical Analysis):** EDA, time series, aggregations
4. ✅ **Trực Quan Hóa (Visualizations):** 7 biểu đồ chi tiết
5. ✅ **Báo Cáo (Reporting):** Báo cáo toàn diện với khuyến nghị

---

##  CẤU TRÚC TỆP DỮ LIỆU ĐẦU RA

### **A. TỆP PHÂN TÍCH (Analysis Files)**

#### 1.  BAOCAO_PHAN_TICH_GIA_CA_PHE.md
- **Loại:** Báo cáo chi tiết (.md)
- **Nội dung:**
  - Tóm tắt điều hành (Executive Summary)
  - Thống kê cơ bản giá cà phê
  - Phân tích theo thời gian (ngày/tuần/tháng)
  - Phân tích động lực giá (Up/Down days)
  - Phân loại tin tức
  - Phân tích nguồn tin (Top 15)
  - Kết luận & khuyến nghị
- **Sử dụng:** Đọc trực tiếp hoặc chuyển đổi sang PDF/HTML

#### 2.  Bảy Biểu Đồ PNG

| File | Mô Tả | Hiển Thị |
|------|-------|---------|
| **chart_01_price_trend.png** | Xu hướng giá + MA7/MA14 | Đường giá + 2 moving average + Peak/Trough |
| **chart_02_daily_change.png** | Biến động hàng ngày | Cột xanh (tăng) & đỏ (giảm), trung bình |
| **chart_03_boxplot_by_month.png** | Phân bố theo tháng | Box plot Q1-Q3, median, outliers |
| **chart_04_weekly_analysis.png** | Thống kê hàng tuần | Mean + Std Dev đối với từng tuần |
| **chart_05_monthly_summary.png** | Tóm tắt hàng tháng | Cột giá TB, min-max range |
| **chart_06_up_down_days.png** | Tăng/Giảm/Đứng Yên | Pie chart + Bar chart so sánh |
| **chart_07_price_distribution.png** | Phân phối giá | Histogram + Mean/Median lines |

### **B. TỆP DỮ LIỆU CSVsummarized (Summary Data)**

#### 1. daily_price_stats.csv
```
Cột: date, price_mean, price_min, price_max, price_std, price_count, sources
Hàng: 61 (số ngày có dữ liệu)
Sử dụng: Phân tích hàng ngày, chart 01-02
```

#### 2. weekly_price_summary.csv
```
Cột: week_end, price_mean, price_min, price_max, price_std
Hàng: 10 (số tuần)
Sử dụng: Phân tích xu hướng hàng tuần, chart 04
```

#### 3. monthly_price_summary.csv
```
Cột: month_end, price_mean, price_min, price_max, price_std, price_count
Hàng: 3 (Jan/Feb/Mar 2026)
Sử dụng: Phân tích so sánh tháng, chart 03 & 05
```

#### 4. coffee_price_timeseries.csv
```
Cột: date, title, price, price_change, price_pct_change, 
      price_ma7, price_ma14, category, source
Hàng: 496 (bản ghi có giá trích xuất được)
Sử dụng: Dữ liệu gốc cho tất cả phân tích, ML models
```

### **C. TỆP GỐC & XỬ LÝ (Source & Processing Files)**

#### 1. data_cafe.csv (Gốc)
- **Kích cỡ:** 2,875 bản ghi × 4 cột
- **Cột:** title, time, source, link (từ web scraping)
- **Nguyên bản từ:** 85 tờ báo tiếng Việt

#### 2. data_cafe_processed.csv (Đã xử lý)
- **Kích cỡ:** 2,875 bản ghi × 12 cột
- **Thêm cột:** date, year, month, day, week, price, price_count, category, title_length
- **Được tạo bởi:** data_processing.py

### **D. SCRIPT CHÍNH (Main Scripts)**

#### 1. data_processing.py (ETL Pipeline)
```python
Chức năng:
  - Tải CSV
  - Trích xuất giá bằng regex: pattern "XXX.XXX đ/kg"
  - Lọc phạm vi: 50,000 - 200,000 đ/kg
  - Gán loại tin (8 danh mục)
  - Tách date components
  - Tính MA7, MA14, price_change
  - Xuất CSV đã xử lý

Chạy: python data_processing.py
Output: data_cafe_processed.csv
```

#### 2. run_full_analysis_simple.py (Terminal Analysis)
```python
Chức năng:
  - Phân tích thống kê đầy đủ
  - Không phụ thuộc matplotlib (pure pandas)
  - In báo cáo chi tiết ra console
  - Xuất 4 file CSV summary

Chạy: python run_full_analysis_simple.py
Output: 
  - daily_price_stats.csv
  - weekly_price_summary.csv
  - monthly_price_summary.csv
  - coffee_price_timeseries.csv
```

#### 3. create_visualizations.py (Chart Generator)
```python
Chức năng:
  - Tạo 7 biểu đồ PNG từ dữ liệu CSV
  - Font support cho tiếng Việt
  - Độ phân giải cao (300 DPI)

Chạy: python create_visualizations.py
Output: 7 × chart_*.png files
```

#### 4. Phan_tich_gia_ca_phe.ipynb (Jupyter Notebook)
```
Cấu trúc: 17 cells
  - Markdown headers (6 cells)
  - Import & data loading (2 cells)
  - Statistical analysis (3 cells)
  - Visualizations (6 cells)

Sử dụng: Jupyter Lab hoặc VS Code
```

---

##  HƯỚNG DẪN SỬ DỤNG

### **1️⃣ Chạy Toàn Bộ Pipeline**

```bash
# Bước 1: Xử lý dữ liệu (tạo data_cafe_processed.csv)
python data_processing.py

# Bước 2: Phân tích thống kê (tạo 4 file CSV summary)
python run_full_analysis_simple.py

# Bước 3: Tạo biểu đồ (tạo 7 file PNG)
python create_visualizations.py

# Bước 4: Đọc báo cáo
markdown BAOCAO_PHAN_TICH_GIA_CA_PHE.md
```

### **2️⃣ Sử Dụng Jupyter Notebook**

```bash
# Mở Jupyter
jupyter notebook Phan_tich_gia_ca_phe.ipynb

# Chọn Python kernel
# Chạy từng cell bằng Shift+Enter
```

### **3️⃣ Sử Dụng Công Cụ Phân Tích**

```python
import pandas as pd

# Đọc dữ liệu để phân tích thêm
df = pd.read_csv('coffee_price_timeseries.csv')
df_daily = pd.read_csv('daily_price_stats.csv')

# Ví dụ: Tìm ngày giá cao nhất
print(df.loc[df['price'].idxmax()])

# Ví dụ: Tính ROI giai đoạn
roi = (df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0] * 100
print(f"ROI: {roi:.2f}%")
```

---

##  KẾT QUẢ CHÍNH

### **Thống Kê Tóm Tắt**

| Chỉ Số | Giá Trị |
|-------|--------|
| **Tổng bản ghi gốc** | 2,875 |
| **Bản ghi có giá** | 496 (17.3%) |
| **Giá trung bình** | 100,782 đ/kg |
| **Giá cao nhất** | 152,000 đ/kg (29/01) |
| **Giá thấp nhất** | 90,400 đ/kg (17/03) |
| **Biến động %** | -6.9% toàn kỳ |
| **Hệ số CV** | 12.1% (ổn định) |
| **Ngày tăng** | 142 (28.7%) |
| **Ngày giảm** | 144 (29.1%) |
| **Số tờ báo** | 85 |
| **Giai đoạn** | 66 ngày |

### **Top Findings**

✅ **Xu hướng chung:** Giảm trên toàn kỳ  
✅ **Điểm mạnh:** Tháng 1-2 tăng mạnh (lên 152k)  
✅ **Điểm yếu:** Tháng 3 giảm mạnh (xuống 90.4k)  
✅ **Độ tin cậy:** Cao - từ 85 nguồn tin  
✅ **Dữ liệu:** Đủ để phân tích (8.1 tin/ngày)

---

## ️ YÊU CẦU KỸ THUẬT

### **Dependencies**

```
Python 3.7+
pandas >= 1.0
numpy >= 1.18
matplotlib >= 3.3
seaborn >= 0.11
```

### **Cài Đặt**

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### **Môi Trường Hỗ Trợ**

- ✅ Windows (PowerShell)
- ✅ Mac (Terminal)
- ✅ Linux (Bash)
- ✅ VS Code + Python Extension
- ✅ Jupyter Lab/Notebook

---

##  Khả Năng Mở Rộng

### **Nâng cấp có thể:**

1. **Machine Learning**
   - ARIMA forecasting cho giá cà phê
   - Anomaly detection (outlier prices)
   - Sentiment analysis trên tiêu đề tin

2. **Dữ Liệu**
   - Thêm dữ liệu lịch sử (6-12 tháng)
   - Integrate giá từ các nguồn khác
   - Thêm biến kinh tế (USD/VND, weather, etc.)

3. **Visualizations**
   - Dashboard interative (Plotly/Dash)
   - Real-time monitoring (Streamlit)
   - 3D surface plots

4. **Báo Cáo**
   - Automated daily reports
   - Email notifications
   - PDF export

---

##  Quy Trình Khai Phá Dữ Liệu Web (Web Mining Pipeline)

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 1: DATA COLLECTION (Thu Thập)                          │
│ Scrapy spiders --> 85 tờ báo --> 2,875 bản ghi                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ BƯỚC 2: DATA PROCESSING (Xử Lý)                             │
│ Regex extraction --> Price validation --> Feature engineering   │
│ 496 bản ghi hữu ích (17.3%)                                │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ BƯỚC 3: EXPLORATORY DATA ANALYSIS (EDA)                     │
│ Descriptive statistics --> Time series --> Aggregations         │
│ Daily/Weekly/Monthly summaries                             │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ BƯỚC 4: VISUALIZATION (Trực Quan Hóa)                       │
│ 7 biểu đồ PNG --> Trends, Distribution, Dynamics             │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ BƯỚC 5: REPORTING & INSIGHTS (Báo Cáo)                      │
│ Comprehensive markdown report --> Recommendations             │
└─────────────────────────────────────────────────────────────┘
```

---

##  Lưu Trữ & Backup

**Tất cả tệp được tạo trong:** `c:\Users\ADMIN\crawl_quotes\`

**Khuyến nghị:**
-  Backup folder project hàng tuần
-  Commit code lên Git repository
-  Lưu biểu đồ vào cloud storage

---

## ❓ Câu Hỏi Thường Gặp

**Q: Tại sao chỉ 17.3% bản ghi có giá?**  
A: Giá được trích xuất từ tiêu đề tin bằng regex. Không phải tất cả tin đều chứa giá cụ thể.

**Q: Làm thế nào để cải thiện tỷ lệ trích xuất?**  
A: Sử dụng NLP/ML models (Named Entity Recognition) để trích xuất từ ngữ cảnh phức tạp.

**Q: Có thể dự báo giá tương lai không?**  
A: Có - sử dụng ARIMA hoặc Facebook Prophet cho time series forecasting.

**Q: Dữ liệu có độ trễ không?**  
A: Tin báo thường công bố sau khi giá thay đổi 1-2 ngày.

**Q: Làm sao để tự động chạy hàng ngày?**  
A: Dùng Task Scheduler (Windows) hoặc Cron (Linux) để schedule scripts.

---

##  Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra console output tìm lỗi
2. Xác nhận dữ liệu gốc (data_cafe.csv) có bộ
3. Cài lại dependencies: `pip install --upgrade pandas matplotlib`

---

## ✅ Checklist Hoàn Thành

- ✅ Dữ liệu được thu thập (2,875 bản ghi từ 85 tờ báo)
- ✅ Pipeline ETL được xây dựng (data_processing.py)
- ✅ Phân tích thống kê hoàn thành (4 CSV summaries)
- ✅ 7 biểu đồ được tạo (PNG 300 DPI)
- ✅ Báo cáo chi tiết được viết (markdown)
- ✅ Jupyter notebook được chuẩn bị (17 cells)
- ✅ Tất cả script được test và verify
- ✅ Tài liệu được hoàn thành

---

** Dự Án Hoàn Thành Đầy Đủ!**

*Ngày hoàn thành: Tháng Ba 2026*  
*Mô đun: Khai Phá Dữ Liệu Web (Web Data Mining)*  
*Trạng thái: ✅ READY FOR PRESENTATION*
