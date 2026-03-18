# Crawl Quotes - Multi-Site Vietnamese News Crawler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Scrapy 2.0+](https://img.shields.io/badge/scrapy-2.0+-green.svg)](https://scrapy.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)

A professional Scrapy-based web crawler to search and extract news articles about coffee (cà phê) and related commodities from multiple Vietnamese news websites. Includes intelligent filtering, automatic deduplication, CSV export, and type hints for production use.

**Expected Output**: 5,000–10,000+ coffee-related articles per crawl across 4 Vietnamese news sites  
**Crawl Time**: 30–60 minutes (with respectful delays)  
**Data Quality**: Coffee-filtered (only relevant articles saved)

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/crawl_quotes.git
cd crawl_quotes

# Install dependencies
pip install -r requirements.txt
```

### Run Crawler

**Default (searches: cà phê, robusta, arabica):**

```bash
python run_news_search.py
```

**Custom keywords:**

```bash
python run_news_search.py "giá cà phê" "nông sản" "tây nguyên"
```

**Single keyword:**

```bash
python run_news_search.py cafe
```

Output saved to: `data_cafe.csv`

## 📋 Table of Contents

- [Features](#-features)
- [Supported Sites](#-supported-sites)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Output Format](#-output-format)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- ✅ **Multi-site crawling**: 4 major Vietnamese news sources
- ✅ **Multi-keyword search**: Default searches cà phê, robusta, arabica (customizable)
- ✅ **Coffee content filtering**: Only saves articles with coffee-related keywords
- ✅ **Intelligent pagination**: Up to 130+ pages per site (50×baomoi + 30×vnexpress + 30×vtcnews + 20×dantri)
- ✅ **Automatic deduplication**: Pipeline removes duplicate links
- ✅ **Type hints**: Full Python type annotations for IDE support
- ✅ **Comprehensive docstrings**: Professional documentation for every method
- ✅ **CSV export**: Clean UTF-8 encoded output
- ✅ **Request headers**: Automatic User-Agent & Accept headers to avoid 406 blocks
- ✅ **Respectful crawling**: Configurable delays (default 1s) to avoid overloading servers

## 🗂️ Supported Sites

| Site | Type | Pages | Notes |
|------|------|-------|-------|
| **baomoi.com** | News aggregator | 50/keyword | Best metadata, reliable selectors |
| **vnexpress.net** | News portal | 30/keyword | Large archive, generic fallback needed |
| **vtcnews.vn** | News portal | 30/keyword | Good coverage, dynamic content possible |
| **dantri.com.vn** | News portal | 20/keyword | Business-focused, fewer coffee articles |

## ⚙️ Configuration

Edit `crawl_quotes/settings.py`:

```python
# Crawling behavior
CONCURRENT_REQUESTS_PER_DOMAIN = 1  # Requests in parallel per domain (default: 1)
DOWNLOAD_DELAY = 1                  # Seconds between requests (default: 1)

# Output
FEEDS = {
    'data_cafe.csv': {
        'format': 'csv',
        'encoding': 'utf-8',
    }
}

# Request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...'
}

# Pipelines (deduplication enabled)
ITEM_PIPELINES = {
    'crawl_quotes.pipelines.DedupePipeline': 300,
}
```

## 📖 Usage

### Python Runner (Recommended for Windows)

```bash
# Default keywords
python run_news_search.py

# Custom keywords (space or comma separated)
python run_news_search.py "chủ đề 1" "chủ đề 2"

# Single keyword
python run_news_search.py cafe
```

### Scrapy CLI

```bash
# Default
scrapy crawl news_search

# Custom keywords (Python syntax)
scrapy crawl -a keywords="['cà phê', 'robusta']" news_search

# With CSV output
scrapy crawl -a keywords="['cà phê']" -o results.csv -t csv news_search
```

## 📊 Output Format

Output file: `data_cafe.csv`

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| `title` | string | "Giá cà phê hôm nay tăng 200 đ/kg" | Article headline |
| `link` | string | "https://baomoi.com/..." | Full article URL |
| `time` | datetime | "2026-03-18T10:55:00+07:00" | Publication timestamp |
| `source` | string | "Báo Đà Nẵng" | News source/publication |
| `site` | string | "baomoi.com" | Website domain |

### Example Data

```csv
title,link,time,source,site
"Giá cà phê hôm nay 18/3: Tăng nhẹ 200 đ/kg",https://baomoi.com/gia-ca-phe-hom-nay-18-3-2026-tang-nhe-200-dong-kg-c54719622.epi,2026-03-18T10:55:00+07:00,Báo Đà Nẵng,baomoi.com
"Thị trường cà phê phục hồi, Robusta và Arabica đồng loạt bứt phá",https://baomoi.com/thi-truong-ca-phe-phuc-hoi-robusta-va-arabica-dong-loat-but-pha-c54720025.epi,2026-03-18T10:30:00+07:00,Tạp chí Doanh nhân Sài Gòn,baomoi.com
```

### Analyze Results

**PowerShell:**

```powershell
# Count articles
(Import-Csv data_cafe.csv -Encoding UTF8).Count

# View first 10
Import-Csv data_cafe.csv -Encoding UTF8 | Select-Object -First 10

# Count by site
Import-Csv data_cafe.csv -Encoding UTF8 | Group-Object site | ForEach-Object { "$($_.Name): $($_.Count)" }
```

**Python:**

```python
import pandas as pd

df = pd.read_csv('data_cafe.csv', encoding='utf-8')
print(f"Total articles: {len(df)}")
print(f"\nArticles by site:")
print(df['site'].value_counts())
print(f"\nFirst 5 articles:")
print(df.head())
```

## ⚡ Performance

| Metric | Value |
|--------|-------|
| **Total URLs crawled** | ~130+ per keyword × all sites |
| **Expected articles** | 5,000–10,000+ (depends on keyword popularity) |
| **Crawl time** | 30–60 minutes |
| **Data deduplicated** | Pipeline removes ~5–10% duplicates |
| **CPU usage** | Low (single-threaded, respectful) |
| **Memory usage** | <100 MB (includes ~3-5K unique URLs cache) |

### Speed Optimization

To crawl faster (use responsibly):

```python
# settings.py
CONCURRENT_REQUESTS_PER_DOMAIN = 4  # Up from 1
DOWNLOAD_DELAY = 0.5                 # Down from 1
```

**Warning**: Too aggressive crawling may get your IP blocked. Recommended defaults: `CONCURRENT=1`, `DELAY=1`

## 🔧 Troubleshooting

### ❌ Empty or Low Results

1. **Check keyword popularity**: Some keywords may have fewer articles
2. **Verify coffee keywords**: Edit `crawl_quotes/spiders/news_search_spider.py`:
   ```python
   coffee_keywords = [
       'cà phê', 'robusta', 'arabica', ...  # Add more as needed
   ]
   ```
3. **Increase pagination**: Change `range(2, 51)` to `range(2, 101)` for more pages
4. **Add more sites**: Add new URLs in `start_requests()`

### ❌ 406 Not Acceptable Errors

The spider sends proper headers. If still blocked:
- Increase `DOWNLOAD_DELAY` to 2–3 seconds
- Some sites require JavaScript (Selenium/Playwright needed)
- Check if site's `robots.txt` blocks crawling

### ❌ Unicode Issues in Excel

CSV is UTF-8 encoded. In Excel:
- **File → Open → Select `data_cafe.csv` → File Origin: UTF-8**
- Or use **Data → From Text/CSV** dialog

### ❌ CSV File Truncated

The spider may still be writing. Wait for logs to show "Spider closed (finished)" before checking the file.

## 📁 Project Structure

```
crawl_quotes/
├── crawl_quotes/
│   ├── spiders/
│   │   ├── news_search_spider.py    # Main multi-site spider (full docstrings)
│   │   ├── baomoi_spider.py         # Single-site legacy spider
│   │   └── quotes_spider.py         # Demo spider
│   ├── settings.py                   # Scrapy settings (FEEDS, headers, pipelines)
│   ├── pipelines.py                  # DedupePipeline class
│   ├── items.py
│   ├── middlewares.py
│   ├── __init__.py
│   └── __pycache__/
├── run_news_search.py                # Python runner (Windows-friendly)
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── .gitignore                        # Git ignore rules
├── scrapy.cfg                        # Scrapy project config
├── data_cafe.csv                     # Output (generated after crawl)
└── *.csv                            # Other data files
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new sites
- Improving coffee keyword filters
- Fixing issues
- Enhancing selectors

TL;DR:
1. Fork & clone
2. Create feature branch: `git checkout -b feature/your-feature`
3. Test: `python run_news_search.py cafe`
4. Commit: `git commit -m "Add: description"`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Scrapy](https://scrapy.org/) web scraping framework
- Vietnamese news sources: baomoi, vnexpress, vtcnews, dantri
- Inspired by real-world coffee market research needs

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/crawl_quotes/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/crawl_quotes/discussions)
- **Email**: your-email@example.com

---

**Happy crawling! ☕📊**

*Last updated: March 18, 2026*
