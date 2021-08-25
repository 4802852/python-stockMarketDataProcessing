import requests
from bs4 import BeautifulSoup as soup
from slack.slack import *

url = "https://finance.naver.com/marketindex/"
res = requests.get(url)
html = soup(res.text, "html.parser")

nation = html.select("a.head > h3.h_lst")
value = html.select("div.head_info > span.value")
change = html.select("div.head_info > span.change")
updown = html.select("div.head_info > span.blind")

for i in range(len(nation)):
    if nation[i].string in ["미국 USD", "달러인덱스"]:
        if updown[i].string == "상승":
            mark = "↑"
        elif updown[i].string == "하락":
            mark = "↓"
        else:
            mark = "-"
        mesg = [nation[i].string, value[i].string, "/", change[i].string, mark]
        mesg = " ".join(mesg)
        to_slack(mesg, "#exchange-rate")
