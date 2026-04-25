import requests, urllib.parse, re, sys
queries = sys.argv[1:]
for q in queries:
    url='https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)
    print('\n### QUERY:', q)
    html=requests.get(url, timeout=20, headers={'User-Agent':'Mozilla/5.0'}).text
    for m in re.finditer(r'nofollow" class="result__a" href="(.*?)".*?>(.*?)</a>', html):
        href=m.group(1)
        title=re.sub('<.*?>','',m.group(2))
        print(title)
        print(href)
    print('---')