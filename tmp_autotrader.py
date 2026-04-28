import requests,re,json
from bs4 import BeautifulSoup
url='https://www.autotrader.co.uk/car-search?advertising-location=at_cars&make=Mercedes-Benz&model=GLA&variant=GLA250e&sort=price-asc&year-from=2023&postcode=SW1A%201AA'
html=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
print('len',len(html))
# find vehicle search results in JSON
for pat in [r'__NEXT_DATA__', r'"colour":"(.*?)"', r'/car-details/\d+']:
    m=re.findall(pat, html)
    print(pat, len(m), m[:5])
# print around first car-details
idx=html.find('/car-details/')
print('idx', idx)
print(html[idx:idx+1000])
