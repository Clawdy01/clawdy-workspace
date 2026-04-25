import requests, re
url='https://www.autoscout24.nl/lst/mercedes-benz/gla-250/bc_blauw?atype=C&fregfrom=2024&ustate=N%2CU&vehtyp=10&powertype=kw&cy=D%2CNL%2CBE'
html=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=20).text
for m in re.finditer(r'<article id="([0-9a-f-]{36})".*?</article>', html, re.S):
    aid=m.group(1); block=m.group(0)
    if 'Electric/Gasoline' not in block and 'Elektrisch/Benzine' not in block:
        continue
    title=re.search(r'ListItemTitle_title__sLi_x">(.*?)</span>', block)
    subtitle=re.search(r'ListItemTitle_subtitle__V_ao6">\s*<!-- -->?(.*?)<!-- -->?\s*</span>', block, re.S)
    price=re.search(r'data-price="(\d+)"', block)
    reg=re.search(r'data-first-registration="([^"]+)"', block)
    km=re.search(r'data-mileage="([^"]+)"', block)
    addr=re.search(r'data-testid="dealer-address"[^>]*>(.*?)</span>', block)
    seller=re.search(r'data-testid="dealer-company-name"[^>]*>(.*?)</span>', block)
    links=re.findall(r'(/aanbod/[^"\']+|/offers/[^"\']+)', block)
    subtitle_txt=(subtitle.group(1).strip() if subtitle else '').replace('\n',' ')
    color=''
    if links:
        parts=links[0].split('-')
        if len(parts)>2: color=parts[-2]
    print(aid, price.group(1) if price else '', reg.group(1) if reg else '', km.group(1) if km else '', color, seller.group(1) if seller else '', addr.group(1) if addr else '')
    print(' ', (title.group(1) if title else '') + ' ' + subtitle_txt)
    if links: print(' ', 'https://www.autoscout24.nl'+links[0] if links[0].startswith('/aanbod/') else 'https://www.autoscout24.com'+links[0])
    print()