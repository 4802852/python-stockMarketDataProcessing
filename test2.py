import requests
from bs4 import BeautifulSoup as soup
from slack.slack import *
import pandas as pd

url = "https://finance.naver.com/marketindex/"
res = requests.get(url)
df = pd.read_html(res.text)

print(df)
