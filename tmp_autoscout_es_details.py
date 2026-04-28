import requests,re,json
url='https://www.autoscout24.es/lst/mercedes-benz/gla-250/bc_azul?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU&vehtyp=10&fuel=2'
h=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',h)
data=json.loads(m.group(1))
for x in data['props']['pageProps']['listings']:
    print(x['id'], x['url'], x['price']['priceFormatted'], [d['data'] for d in x['vehicleDetails']])
