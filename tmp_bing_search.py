import requests, bs4, urllib.parse
queries = [
    'Mercedes GLA 250e blue 2024 for sale',
    'Mercedes GLA 250e spectral blue dealer',
    'site:autoscout24.com/offers Mercedes GLA 250e blue',
    'site:cars.ie Mercedes GLA 250e blue',
    'site:autotrader.co.uk Mercedes GLA250e blue'
]
for q in queries:
    url='https://www.bing.com/search?q='+urllib.parse.quote(q)
    r=requests.get(url, timeout=20, headers={'User-Agent':'Mozilla/5.0'})
    print('\nQUERY:', q, 'status', r.status_code)
    soup=bs4.BeautifulSoup(r.text, 'html.parser')
    for li in soup.select('li.b_algo')[:8]:
        a=li.select_one('h2 a')
        sn=li.select_one('.b_caption p')
        print('-', a.get_text(' ', strip=True) if a else '')
        print(' ', a.get('href') if a else '')
        print(' ', sn.get_text(' ', strip=True) if sn else '')
