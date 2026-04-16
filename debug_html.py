import requests
from bs4 import BeautifulSoup

# Test một URL
url = 'https://baomoi.com/xa-na-son-ra-quan-dao-ho-trong-mac-ca-ca-phe-nam-2026-c54720700.epi'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f'Testing: {url}\n')

resp = requests.get(url, headers=headers, timeout=10)
print(f'Status: {resp.status_code}')
print(f'Content length: {len(resp.text)} bytes\n')

if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Check for article structures
    article = soup.find('article')
    has_article = "found" if article else "not found"
    print(f'  Article tag: {has_article}')
    
    div_article = soup.find('div', class_='article-content')
    has_div = "found" if div_article else "not found"
    print(f'  Div.article-content: {has_div}')
    
    div_main = soup.find('div', id='content')
    has_content = "found" if div_main else "not found"
    print(f'  Div#content: {has_content}')
    
    main = soup.find('main')
    has_main = "found" if main else "not found"
    print(f'  Main tag: {has_main}')
    
    # Count paragraphs
    paras = soup.find_all('p')
    print(f'\n  Total P tags: {len(paras)}')
    
    # Show first 3 paragraphs
    if paras:
        print(f'\n  First 3 paragraphs:')
        for i, p in enumerate(paras[:3]):
            text = p.get_text().strip()[:70]
            is_long = len(p.get_text().strip()) > 70
            suffix = '...' if is_long else ''
            print(f'    {i+1}. {text}{suffix}')
else:
    print('Failed to fetch page')
