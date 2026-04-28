import requests, bs4, urllib.parse
queries = [
    'site:mobile.de Mercedes GLA 250 e spectraublau 2024',
    'site:mobile.de Mercedes GLA 250 e blau AMG Line 2024',
    'site:autoscout24.com/offers Mercedes GLA 250 e blue 2025',
    'site:cars.ie Mercedes GLA 250 e blue 2024',
    'site:autotrader.co.uk Mercedes GLA250e blue 2024',
    'site:heycar.co.uk Mercedes GLA 250e blue',
    'site:automarket.lu Mercedes-Benz GLA 250 e blue'
]
for q in queries:
    url='https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)
    r=requests.get(url, timeout=20, headers={'User-Agent':'Mozilla/5.0'})
    print('\nQUERY:', q)
    soup=bs4.BeautifulSoup(r.text, 'html.parser')
    for a in soup.select('.result')[:8]:
        title=a.select_one('.result__title')
        link=a.select_one('.result__title a')
        sn=a.select_one('.result__snippet')
        href=link.get('href') if link else ''
        print('-', title.get_text(' ', strip=True) if title else '')
        print(' ', href)
        print(' ', sn.get_text(' ', strip=True) if sn else '')
