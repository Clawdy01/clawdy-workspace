import requests,re
from bs4 import BeautifulSoup
url='https://www.cars.ie/cars/mercedes-benz/gla-class/250e?sort=Newest'
html=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=20).text
print('len',len(html))
print(html[:500])
soup=BeautifulSoup(html,'html.parser')
for a in soup.select('a')[:20]:
    href=a.get('href','')
    text=a.get_text(' ',strip=True)
    if 'listing-' in href or 'gla' in href.lower():
        print(href, text[:120])
