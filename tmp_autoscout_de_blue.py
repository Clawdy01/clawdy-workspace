import requests,re,json
urls=[
'https://www.autoscout24.de/lst/mercedes-benz/gla-250/ve_e/bc_blau?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU',
'https://www.autoscout24.es/lst/mercedes-benz/gla-250/bc_azul?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU&vehtyp=10&fuel=2',
'https://www.autoscout24.fr/lst/mercedes-benz/gla-250/ve_e/bc_bleu?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU',
'https://www.autoscout24.nl/lst/mercedes-benz/gla-250/ve_e/bc_blauw?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU'
]
for url in urls:
    h=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
    m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',h)
    print('\nURL',url,'hasnext',bool(m),'len',len(h))
    if not m: continue
    data=json.loads(m.group(1))
    lst=data['props']['pageProps'].get('listings') or []
    print('count',len(lst))
    for x in lst[:8]:
        print(x['id'], x['url'], x.get('price',{}).get('priceFormatted'))
