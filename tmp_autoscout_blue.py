import requests,re,json
url='https://www.autoscout24.com/lst/mercedes-benz/gla-250/ve_e?atype=C&desc=0&fregfrom=2023&sort=standard&ustate=N%2CU&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL'
html=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
data=json.loads(m.group(1))
for x in data['props']['pageProps']['listings']:
    if 'blue' in x['url'] or 'azul' in x['url'] or 'blau' in x['url']:
        print(x['id'], x['url'], x['price']['priceFormatted'], x['vehicleDetails'][0]['data'], x['vehicleDetails'][2]['data'])
