# Contributing to Crawl Quotes

Thank you for your interest in contributing to Crawl Quotes! Here's how you can help.

## How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/YOUR_USERNAME/crawl_quotes.git
cd crawl_quotes
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

#### Adding a New Site
1. Create a new spider method in `crawl_quotes/spiders/news_search_spider.py`
2. Add the site to `allowed_domains` and `start_requests()`
3. Implement site-specific parsing (e.g., `parse_yoursite()`)
4. Test with: `python run_news_search.py`

#### Adding Coffee Keywords
Edit `coffee_keywords` list in `news_search_spider.py`:
```python
coffee_keywords = [
    'cà phê', 'robusta', 'arabica', 'your_keyword', ...
]
```

#### Improving Filtering
Update `_is_coffee_related()` method for better article relevance

### 4. Test Your Changes
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run a test crawl
python run_news_search.py cafe

# Check output
Import-Csv data_cafe.csv -Encoding UTF8 | Select-Object -First 10
```

### 5. Commit & Push
```bash
git add .
git commit -m "Add: Description of your changes"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to GitHub and create a PR
- Describe what you changed and why
- Wait for review

## Code Style

- Use **snake_case** for functions and variables
- Use **PascalCase** for class names
- Add docstrings to all public methods
- Keep lines under 100 characters
- Use type hints where possible

Example:
```python
def parse_baomoi(self, response: Response) -> Iterator[dict]:
    """Parse baomoi.com search results with coffee keyword filtering.
    
    Args:
        response: Scrapy Response object
        
    Yields:
        Dictionary with title, link, time, source, site
    """
    pass
```

## Reporting Issues

Found a bug? Open an Issue on GitHub with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your OS and Python version

## Questions?

Feel free to open a Discussion or Issue for help!

## License

By contributing, you agree your work will be licensed under MIT License.
