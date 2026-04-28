import requests,re,json
urls=[
'https://www.autoscout24.com/lst/mercedes-benz/gla-250/ve_e?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&bc=2&powertype=kw',
'https://www.autoscout24.com/lst/mercedes-benz/gla-250/ve_e?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&bc=2&color=2',
'https://www.autoscout24.com/lst/mercedes-benz/gla-250/ve_e/bc_blue?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL'
]
for url in urls:
    html=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
    m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    data=json.loads(m.group(1))
    print('\nURL',url)
    for x in data['props']['pageProps']['listings'][:8]:
        print(x['id'], x['url'])
