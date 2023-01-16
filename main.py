# Parcer for Auto.ru magazine news. Return file with articles for keyword
# for exapmple, use key word Toyota to get articles about Toyota cars
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from csv import DictWriter

#suppress SSL sertificate error
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

url_base="https://mag.auto.ru/theme/news/?page="
curr_page = 1

search_str = input("key word for search: ")
Next_page = True
headers = {
"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding" : "gzip, deflate, br",
"Accept-Language" : "en-US,en;q=0.9,ru;q=0.8",
"Cache-Control" : "max-age=0",
"Connection" : "keep-alive",
"Cookie" : "suid=63d8a4b4da8200444bd96bc8fd48851a.4227164c27213581f9126f5408248788; autoru_sid=a%3Ag63c45e8826rkdmrd7l304ou7mbhjs5u.fdfc316f4b4177c351558aa5cc903f8b%7C1673813640134.604800.m18SPB0-6f522iW44qQMdg.jc_QKwQeDYBxA6UkLw7RhIYtDnvkqMGg7NZnfVBUrZg; autoruuid=g63c45e8826rkdmrd7l304ou7mbhjs5u.fdfc316f4b4177c351558aa5cc903f8b; autoru_gdpr=1; _csrf_token=7d86ad9c4608583187de75767e8071c49166064eb4f2c68e; from=direct; yuidlt=1; yandexuid=2998309091672660451; gdpr_popup=1; Session_id=3:1673813650.5.0.1672660623376:d8PhpQ:36.1.2:1|670956.0.2|61:10010345.459297.B7VwgFL3MmPsxdrOJ8UJu5JuPtc; yandex_login=Roger2001; ys=udn.cDpSb2dlcjIwMDE%3D#c_chck.462272866; i=ZoFeuNmwJ9Lzd4y0wzVxhDTjFpDalW+IxTCjI6ekprri8IXL+acOpgGg3tURzTyXpVK40D5LsZqp8VuQvaEALHXJnjU=; mda2_beacon=1673813650517; gdpr=0; hide-new-car-promo=true; _ym_uid=16738136571427253; from_lifetime=1673814020297; layout-config={\"screen_height\":864,\"screen_width\":1536,\"win_width\":753,\"win_height\":721}; _ym_d=1673894880; _yasc=89Qy0PRiSGicAdfnHBlJuBcIw3JuEfbeDimbe5Mo6Bq/Fy+z+Ie+9m52pzsLN2I=; _ym_visorc=b; _ym_isad=2; mindboxDeviceUUID=c38e202f-5d2e-4270-889b-bc482a0e26f4; directCrm-session=%7B%22deviceGuid%22%3A%22c38e202f-5d2e-4270-889b-bc482a0e26f4%22%7D; cycada=04rWo+3UaBWKOsGsxImIRAjXK7K9GR/m18cB/V0r2iQ=",
"Host" : "mag.auto.ru",
"sec-ch-ua" : "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
"sec-ch-ua-mobile" : "?0",
"sec-ch-ua-platform" : "Windows",
"Sec-Fetch-Dest" : "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site" : "same-origin",
"Sec-Fetch-User" : "?1",
"Upgrade-Insecure-Requests" : "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

#while Next_page:
url = f'{url_base}{curr_page}'
print(url)
req_result = requests.get(url, verify=False, headers=headers)
soup = BeautifulSoup(req_result.text, 'html.parser')
print(soup)
#find Class in soup
span = soup.find('span', class_='register')
print(span)