# Coffee Price Analysis - Web Mining Project

A complete data mining pipeline for analyzing Vietnamese news articles about coffee commodity prices. 
This project demonstrates web scraping, data extraction, statistical analysis, and visualization techniques 
for price trend forecasting.

**Data Volume**: 2,875 news articles from 85 Vietnamese news sources  
**Extracted Records**: 496 articles with identifiable coffee prices (17.3%)  
**Analysis Period**: 66 days (January-March 2026)  
**Status**: Complete and ready for submission

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Methodology](#methodology)
4. [Usage Instructions](#usage-instructions)
5. [Key Findings](#key-findings)
6. [Project Structure](#project-structure)
7. [Installation](#installation)
8. [Troubleshooting](#troubleshooting)
9. [License](#license)

---

## Project Overview

This project implements a complete data mining pipeline with five phases:

1. **Data Collection**: Web scraping Vietnamese news sites using Scrapy
2. **Data Processing**: Extract coffee prices from article headlines using regex
3. **Statistical Analysis**: Calculate descriptive statistics and time series aggregations
4. **Visualization**: Generate professional charts with technical indicators
5. **Reporting**: Create comprehensive analysis reports and recommendations

### Key Statistics

| Metric | Value |
|--------|-------|
| Raw Articles Collected | 2,875 |
| Articles with Extracted Prices | 496 |
| Extraction Success Rate | 17.3% |
| Average Price | 100,782 đ/kg |
| Price Range | 90,400 - 152,000 đ/kg |
| Price Volatility (CV) | 12.1% |
| Price Change (Period) | -6.9% |

---

## Problem Statement

### Objective
Analyze and forecast coffee commodity price trends from Vietnamese news articles using automated extraction techniques.

### Research Questions
- What are the statistical characteristics of coffee prices? (mean, variance, distribution)
- How do prices vary at daily, weekly, and monthly intervals?
- What market sentiment signals can be extracted from price movement patterns?
- Which news sources provide the most reliable price information?

### Expected Outcomes
- Historical price time series with technical indicators (MA7, MA14)
- Statistical analysis revealing market trends and stability
- Visualization making price patterns accessible to stakeholders
- Actionable recommendations for price monitoring

---

## Methodology

### Phase 1: Data Collection (Web Scraping)

**Tools**: Scrapy framework (Python)  
**Target**: 85 Vietnamese news websites across 4 major domains

Implemented spider (`news_search_spider.py`) that:
- Fetches article listings using keyword search
- Extracts headline, publication date, source, and URL
- Filters for coffee-related content automatically
- Removes duplicate articles via deduplication pipeline
- Exports clean data to CSV format (UTF-8 encoding)

**Output**: `data_cafe.csv` (2,875 records)

### Phase 2: Data Processing (ETL)

**Tool**: Python Pandas with regex pattern matching

**Price Extraction Algorithm**:
- Pattern matching for prices in format "XXX.XXX đ/kg" or "XXX đ/kg"
- Validation using domain knowledge: 50,000 - 200,000 đ/kg range
- Result: 496 valid price extractions (17.3%)

**Feature Engineering** (12 new columns):
- Temporal: year, month, day, week_of_month, day_of_week
- Price dynamics: price_change, price_pct_change
- Technical indicators: Moving Average 7-day, Moving Average 14-day
- Categorization: News category (8 types identified)
- Metadata: Source, title_length

**Output**: `data_cafe_processed.csv` (2,875 × 12 columns)

### Phase 3: Data Analysis

**Methods**: Descriptive statistics, time series decomposition

**Statistical Measures**:
- Central tendency: Mean (100,782), Median (98,450), Quartiles (96k, 100k)
- Dispersion: Std Dev (12,212), CV (12.1%), Range (61,600)
- Temporal: Daily/Weekly/Monthly aggregations
- Market dynamics: Up days (28.7%), Down days (29.1%), Flat days (42.2%)

**Time Series Levels**:
- Daily: 61 days with recorded prices
- Weekly: 10 weeks aggregated
- Monthly: 3 months (Jan/Feb/Mar 2026)

**Results**: 4 summary CSV files exported

### Phase 4: Visualization

**Tool**: Matplotlib with high-resolution output (300 DPI PNG)

Generated 7 charts:

1. **Price Trend with Moving Averages** - Shows daily prices with MA7 and MA14 smoothing
2. **Daily Change Distribution** - Bar chart of up/down price movements
3. **Monthly Distribution (Box Plot)** - Quartile analysis by month
4. **Weekly Analysis** - Mean prices with volatility indicators
5. **Monthly Summary** - Min/max/mean comparison across 3 months
6. **Up/Down Days** - Pie and bar chart of market direction
7. **Price Distribution** - Histogram showing price concentration

### Phase 5: Reporting

Generated comprehensive documentation:
- Analysis Report: 20,000+ word detailed findings
- Technical Guide: Implementation details and methodology
- Project Summary: Quick reference and FAQs
- File Index: Complete inventory of deliverables

---

## Usage Instructions

### Installation

```bash
pip install -r requirements.txt
```

### Step 1: Web Scraping (Optional - Data Already Provided)

```bash
python run_news_search.py
```

Generates: `data_cafe.csv`

### Step 2: Data Processing

```bash
python data_processing.py
```

Extracts prices and creates features.  
Generates: `data_cafe_processed.csv`

### Step 3: Statistical Analysis

```bash
python run_full_analysis_simple.py
```

Calculates statistics and exports summaries.  
Generates: 
- `daily_price_stats.csv`
- `weekly_price_summary.csv`
- `monthly_price_summary.csv`
- `coffee_price_timeseries.csv`

### Step 4: Visualization

```bash
python create_visualizations.py
```

Creates 7 professional charts.  
Generates: `chart_01_*.png` through `chart_07_*.png`

### Step 5: Interactive Exploration

```bash
jupyter notebook Phan_tich_gia_ca_phe.ipynb
```

17-cell notebook for step-by-step analysis.

---

## Key Findings

### Price Statistics

| Metric | Value | Interpretation |
|--------|-------|-----------------|
| Mean | 100,782 đ/kg | Baseline price level |
| Std Dev | 12,212 (CV: 12.1%) | Low volatility, stable market |
| Max Price | 152,000 đ/kg | Peak on 29 Jan 2026 |
| Min Price | 90,400 đ/kg | Trough on 17 Mar 2026 |
| Period Return | -6.9% | Downtrend over 66 days |

### Market Dynamics

| Category | Percentage | Count |
|----------|-----------|-------|
| Up Days | 28.7% | 142 days (avg +7,033 đ/kg) |
| Down Days | 29.1% | 144 days (avg -6,982 đ/kg) |
| Flat Days | 42.2% | 209 days (no change) |

**Interpretation**: Market is balanced with roughly equal up/down movements.

### Temporal Patterns

**Monthly Trend**:
- January: 100,869 đ/kg (stable)
- February: 103,059 đ/kg (peak, volatile)
- March: 97,775 đ/kg (declining)

**Trend Indicators**:
- MA7 (short-term): Downward
- MA14 (medium-term): Downward

### Data Quality

| Aspect | Assessment |
|--------|-----------|
| Coverage | 61 days of 66 days (92.4%) |
| Extraction Rate | 496 of 2,875 records (17.3%) |
| Source Diversity | 85 news outlets |
| Price Validity | 99% within domain range |

---

## Project Structure

```
crawl_quotes/
├── README.md                         # This file
├── requirements.txt
├── 
├── DATA PROCESSING
├── data_processing.py                # ETL script: Extract prices, create features
├── run_full_analysis_simple.py       # Analysis script: Statistics and aggregations
├── create_visualizations.py          # Visualization script: Generate 7 charts
├──
├── INPUT DATA
├── data_cafe.csv                     # Raw articles (2,875 records)
├── data_cafe_processed.csv           # Processed with features (2,875 x 12)
├──
├── ANALYSIS OUTPUT
├── coffee_price_timeseries.csv       # Full timeseries (496 records)
├── daily_price_stats.csv             # Daily aggregation (61 days)
├── weekly_price_summary.csv          # Weekly aggregation (10 weeks)
├── monthly_price_summary.csv         # Monthly aggregation (3 months)
├──
├── VISUALIZATION OUTPUT
├── chart_01_price_trend.png
├── chart_02_daily_change.png
├── chart_03_boxplot_by_month.png
├── chart_04_weekly_analysis.png
├── chart_05_monthly_summary.png
├── chart_06_up_down_days.png
├── chart_07_price_distribution.png
├──
├── DOCUMENTATION
├── BAOCAO_PHAN_TICH_GIA_CA_PHE.md   # Full analysis report (20,000+ words)
├── PROJECT_SUMMARY.md               # Technical guide
├── COMPLETION_REPORT.md             # Project checklist
├── FILE_INDEX.md                    # File reference
├── QUICKSTART.md                   # Quick reference
├──
├── SCRAPY CRAWLER (Data Collection)
├── crawl_quotes/
│   ├── spiders/
│   │   ├── news_search_spider.py    # Main spider
│   │   ├── baomoi_spider.py
│   │   └── quotes_spider.py
│   ├── pipelines.py                 # Deduplication
│   ├── settings.py
│   ├── items.py
│   └── middlewares.py
├── run_news_search.py               # Python runner
├──
└── INTERACTIVE ANALYSIS
   └── Phan_tich_gia_ca_phe.ipynb    # Jupyter notebook (17 cells)
```

### File Roles

**Scripts** (in order of execution):
1. `data_processing.py` - Process raw data, extract prices
2. `run_full_analysis_simple.py` - Calculate statistics
3. `create_visualizations.py` - Generate charts

**Data Files**:
- Input: `data_cafe.csv` (raw)
- Processed: `data_cafe_processed.csv`, `coffee_price_timeseries.csv`
- Outputs: 4 CSV summary files

**Documentation**:
- Reports: MBA-level analysis (20+ pages)
- Guides: Usage and implementation details
- Index: Quick reference for all files

---

## Installation

### Requirements

- Python 3.7+
- Pandas 1.3+
- NumPy 1.21+
- Matplotlib 3.4+
- Scrapy 2.0+ (for web scraping)
- Jupyter (optional, for interactive notebook)

### Setup

```bash
# Clone or extract project
cd crawl_quotes

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Troubleshooting

### Script Errors

**Issue**: ModuleNotFoundError for pandas, matplotlib, etc.  
**Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: UnicodeDecodeError when reading CSV files  
**Solution**: Files are UTF-8 encoded. Ensure your editor/terminal supports UTF-8.

### Data Issues

**Issue**: Low price extraction rate (< 10%)  
**Reason**: Prices may not be in headline. Current 17.3% is acceptable for name-based extraction.  
**Solution**: Add body text scraping for better coverage.

**Issue**: Prices outside expected range (under 50k or over 200k)  
**Reason**: Domain knowledge filter validates against commodity market norms.  
**Solution**: Adjust range in `data_processing.py` if needed.

### Visualization Issues

**Issue**: Charts cannot be opened  
**Reason**: PNG files require image viewer.  
**Solution**: Use default image viewer on Windows/Mac or browser.

---

## License

MIT License - See LICENSE file for details

## Completion Status

- Data Collection: COMPLETE
- Data Processing: COMPLETE
- Statistical Analysis: COMPLETE
- Visualization: COMPLETE
- Documentation: COMPLETE
- Ready for Submission: YES

---

**Happy crawling! ☕📊**

*Last updated: March 18, 2026*
