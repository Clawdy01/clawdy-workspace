import requests, bs4, urllib.parse
queries = [
    'Mercedes GLA 250e blue AMG Line dealer Europe',
    'Mercedes GLA 250e spectral blue dealer Europe',
    'Mercedes GLA 250e azul concesionario',
    'Mercedes GLA 250e bleu occasion',
    'Mercedes GLA 250e blauw occasion'
]
for q in queries:
    url='https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)
    r=requests.get(url, timeout=20, headers={'User-Agent':'Mozilla/5.0'})
    print('\nQUERY:', q)
    soup=bs4.BeautifulSoup(r.text, 'html.parser')
    for a in soup.select('.result')[:12]:
        title=a.select_one('.result__title')
        link=a.select_one('.result__title a')
        sn=a.select_one('.result__snippet')
        href=link.get('href') if link else ''
        print('-', title.get_text(' ', strip=True) if title else '')
        print(' ', href)
        print(' ', sn.get_text(' ', strip=True) if sn else '')
