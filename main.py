# Parcer for Auto.ru magazine news. Return file with articles for keyword
# for exapmple, use key word Toyota to get articles about Toyota cars

from bs4 import BeautifulSoup
from datetime import datetime
from requests import get
from csv import DictWriter

url_base="https://mag.auto.ru/theme/news/?page="
curr_page = 1

search_str = input("key word for search = ")

