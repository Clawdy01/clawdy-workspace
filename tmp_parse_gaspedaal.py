import requests, re
url='https://www.gaspedaal.nl/mercedes-benz/gla-klasse/blauw'
html=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=20).text
for m in re.finditer(r'href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
    href=m.group(1)
    txt=re.sub('<.*?>',' ',m.group(2))
    txt=' '.join(txt.split())
    if '250 e' in txt or '250e' in txt or 'Plug-In Hybride' in txt:
        print(txt[:300])
        print(href)
        print('---')