import requests
from bs4 import BeautifulSoup as soup

url = "https://finance.naver.com/marketindex/"
res = requests.get(url)
html = soup(res.text, "html.parser")

nation = html.select_one("a.head > h3.h_lst").string
value = html.select_one("span.value").string

print(nation + value)
