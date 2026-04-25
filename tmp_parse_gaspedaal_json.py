import requests,re,json
h=requests.get('https://www.gaspedaal.nl/mercedes-benz/gla-klasse/blauw',headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
m=re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
obj=json.loads(m.group(1))
for item in obj['itemListElement']:
    itm=item['item']
    name=itm.get('name','')
    if '250 e' in name or '250e' in name:
        print('POS', item['position'])
        print('ID', itm.get('@id'))
        print('NAME', name)
        print('PRICE', itm['offers']['price'])
        print('YEAR', itm.get('productionDate'))
        print('KM', itm['mileageFromOdometer']['value'])
        print('COLOR', itm.get('color'))
        print('SELLER', itm['offers']['seller']['name'])
        print('SELLERURL', itm['offers']['seller'].get('url'))
        print()
