# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# import time
# import csv

main_url = 'http://books.toscrape.com/'
response = requests.get(main_url)
if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    cat_name = [line.text.strip() for line in soup.select("ul > li > ul > li > a")]
    cat_url = [main_url + line["href"] for line in soup.select("ul > li > ul > li > a")]


