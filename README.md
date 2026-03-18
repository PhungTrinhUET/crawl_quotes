# Crawl Quotes - Multi-Site News Crawler

A Scrapy-based web crawler to search and extract news articles about coffee (cà phê) and related commodities from multiple Vietnamese news sites.

## Supported Sites

- **baomoi.com** — Search results with full metadata, paginated (50 pages × multiple keywords)
- **vnexpress.net** — Search results with fallback link parsing (30 pages × multiple keywords)
- **vtcnews.vn** — Search results with fallback link parsing (30 pages × multiple keywords)
- **dantri.com.vn** — Search results (20 pages × multiple keywords)

## Features

- **Multi-keyword search** — Searches for 'cà phê', 'robusta', 'arabica' by default
- **Coffee-related filtering** — Filters articles by coffee keywords in title to avoid off-topic results
- **Massive pagination** — Up to 130+ pages per site (50×baomoi + 30×vnexpress + 30×vtcnews + 20×dantri)
- **Automatic link deduplication** (via pipeline)
- **CSV export** to `data_cafe.csv`
- **Automatic request headers** (User-Agent, Accept, etc.) to avoid 406 blocks
- **Best-effort article title/date extraction** from landing pages

## Installation

```bash
pip install scrapy
```

## Usage

### Option 1: Using the Python runner (recommended for Windows)

Default search (cà phê, robusta, arabica):

```bash
cd c:\Users\ADMIN\crawl_quotes
python run_news_search.py
```

Custom keywords:

```bash
python run_news_search.py "giá cà phê" "nông sản" "tây nguyên"
```

Single keyword:

```bash
python run_news_search.py cafe
```

### Option 2: Using Scrapy CLI

```bash
scrapy crawl -a keywords="['cà phê','robusta']" -o sample.csv -t csv news_search
```

## Output

Results are saved to `data_cafe.csv` with columns:
- `title` — Article title
- `link` — Full article URL
- `time` — Publication timestamp (if available)
- `source` — News source/publication
- `site` — Domain (baomoi.com, vnexpress.net, vtcnews.vn, dantri.com.vn)

**Expected volume**: 5,000–10,000+ articles per run (depending on keyword popularity and page availability)

## Configuration

Edit `crawl_quotes/settings.py` to customize:
- `CONCURRENT_REQUESTS_PER_DOMAIN` — Parallel requests per domain (default: 1)
- `DOWNLOAD_DELAY` — Delay between requests in seconds (default: 1)
- `FEEDS` — Output file path and format
- `DEFAULT_REQUEST_HEADERS` — Request headers (User-Agent, etc.)

## Troubleshooting

### Too much off-topic data

The spider now filters by coffee-related keywords. If you still get unrelated articles, edit `coffee_keywords` in [crawl_quotes/spiders/news_search_spider.py](crawl_quotes/spiders/news_search_spider.py#L10):

```python
coffee_keywords = [
    'cà phê', 'ca phe', 'coffee', 'robusta', 'arabica', 
    'tây nguyên', 'giá nông sản', 'xuất khẩu', 'cà-phê',
    'gia ca phe', 'nong san', 'dak lak', 'lam dong', 'gia lai'
]
```

### 406 Not Acceptable errors

The spider sends proper `User-Agent` and `Accept` headers. If a site still blocks requests:
1. Try adding a delay: `DOWNLOAD_DELAY = 2` in settings.py
2. Some sites may require browser automation (Selenium, Playwright) for JavaScript-heavy content

### Slow crawl speed

By default, `CONCURRENT_REQUESTS_PER_DOMAIN = 1` to be respectful. To speed up (use cautiously):
- Increase `CONCURRENT_REQUESTS_PER_DOMAIN` in `settings.py` to 2–4
- Decrease `DOWNLOAD_DELAY` to 0.5–1 second

### Unicode/Vietnamese character issues

All output is UTF-8 encoded. If you see mojibake in Excel, open the CSV with `UTF-8` encoding selection.

## Project Structure

```
crawl_quotes/
├── spiders/
│   ├── news_search_spider.py    # Main multi-site spider with filtering
│   ├── baomoi_spider.py         # Single-site baomoi crawler (legacy)
│   └── quotes_spider.py         # Demo spider
├── settings.py                   # Scrapy configuration
├── pipelines.py                  # DedupePipeline for link deduplication
├── items.py
├── middlewares.py
├── run_news_search.py            # Python runner (Windows-friendly)
├── README.md                     # This file
└── scrapy.cfg
```

## Example Workflow

```bash
# 1. Run crawl with default keywords (cà phê, robusta, arabica)
cd C:\Users\ADMIN\crawl_quotes
python run_news_search.py

# 2. Monitor progress (watch for "Crawled X pages" in logs)
#    Expected time: 30–60 minutes depending on delays and page count

# 3. Analyze results
Import-Csv data_cafe.csv -Encoding UTF8 | Select-Object -First 20
```

Or using pandas:

```python
import pandas as pd
df = pd.read_csv('data_cafe.csv', encoding='utf-8')
print(f"Total articles: {len(df)}")
print(f"Unique sites: {df['site'].unique()}")
print(df.head(10))

# Count articles by site
print(df['site'].value_counts())
```

## Performance Notes

- **Typical crawl time**: 30–60 minutes for 5,000–10,000 articles (all keywords × all sites × 50–130 pages)
- **Typical results**: 5,000–10,000+ articles depending on keyword popularity
- **Data deduplication**: Pipeline automatically drops duplicate links (rare but possible across keywords)
- **Resource usage**: Low CPU/memory (single-threaded, respectful delays)

## Next Steps

To further enhance results:
1. **Add more keywords** — Edit `start_requests()` to search for more specific terms like "xuất khẩu cà phê", "nông sản Tây Nguyên", etc.
2. **Add more sites** — Add agriculture news sites like agrinews.vn or commodity trade sites
3. **Fine-tune filtering** — Add/remove keywords from `coffee_keywords` based on your specific needs
4. **Auto-summarization** — Use NLP/AI to summarize article content and extract key info (prices, volumes, etc.)

## License

Personal use for educational/research purposes.

