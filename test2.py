import requests
from bs4 import BeautifulSoup as soup
from slack.slack import *
import pandas as pd
import json


url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=23705&pair_id_for_news=23705&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield",
}
data = requests.get(url, headers=headers).json()
last_value = float(data["attr"]["last_value"])
last_close_value = float(data["attr"]["last_close_value"])
change = round(last_value - last_close_value, 3)
change_rate = round(change / last_close_value, 4) * 100
if change > 0:
    mark = "↑"
elif change < 0:
    mark = "↓"
else:
    mark = "-"
mesg = ["미국채10년금리", last_value, "/", change, mark, "(", change_rate, "%", ")"]
print(*mesg)
