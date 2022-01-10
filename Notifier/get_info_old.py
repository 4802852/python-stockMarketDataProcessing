import requests
from bs4 import BeautifulSoup as soup
# import sys
# from os import path

# if __package__ is None:
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#     from slack.slack import *
# else:
#     from ..slack.slack import *


def get_exchange_rate():
    url = "https://finance.naver.com/marketindex/"
    res = requests.get(url)
    html = soup(res.text, "html.parser")

    nation = html.select("a.head > h3.h_lst")
    value = html.select("div.head_info > span.value")
    change = html.select("div.head_info > span.change")
    updown = html.select("div.head_info > span.blind")

    for i in range(len(nation)):
        na = nation[i].string
        va = value[i].string.replace(",", "")
        ch = change[i].string.replace(",", "")
        ud = updown[i].string
        if na == "미국 USD":
            if ud == "상승":
                mark = "↑"
            elif ud == "하락":
                mark = "↓"
            else:
                mark = "-"
            change_rate = round(float(ch) / (float(va) - float(ch)) * 100, 2)
            mesg = [na, "\n     ", va, "/", ch, mark, "(", str(change_rate), "% )"]
            mesg = " ".join(mesg)
    return mesg


def get_dollar_index():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8827&pair_id_for_news=8827&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/currencies/us-dollar-index",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    last_close_value = float(data["attr"]["last_close_value"])
    change = round(last_value - last_close_value, 3)
    change_rate = round(change / last_close_value * 100, 2)
    if change > 0:
        mark = "↑"
    elif change < 0:
        mark = "↓"
        change = -change
    else:
        mark = "-"
    mesg = [
        "달러인덱스\n     ",
        str(last_value),
        "/",
        str(change),
        mark,
        "(",
        str(change_rate),
        "%",
        ")",
    ]
    mesg = " ".join(mesg)
    return mesg


def get_interest():
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
    change_rate = round(change / last_close_value * 100, 2)
    if change > 0:
        mark = "↑"
    elif change < 0:
        mark = "↓"
        change = -change
    else:
        mark = "-"
    mesg = [
        "미국채10년금리\n     ",
        str(last_value),
        "/",
        str(change),
        mark,
        "(",
        str(change_rate),
        "%",
        ")",
    ]
    mesg = " ".join(mesg)
    return mesg


def get_copper():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8831&pair_id_for_news=8831&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/commodities/copper",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    last_close_value = float(data["attr"]["last_close_value"])
    change = round(last_value - last_close_value, 3)
    change_rate = round(change / last_close_value * 100, 2)
    if change > 0:
        mark = "↑"
    elif change < 0:
        mark = "↓"
        change = -change
    else:
        mark = "-"
    mesg = [
        "구리원자재\n     ",
        str(last_value),
        "/",
        str(change),
        mark,
        "(",
        str(change_rate),
        "%",
        ")",
    ]
    mesg = " ".join(mesg)
    return mesg


def get_wti_oil():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8849&pair_id_for_news=8849&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/commodities/crude-oil",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    last_close_value = float(data["attr"]["last_close_value"])
    change = round(last_value - last_close_value, 3)
    change_rate = round(change / last_close_value * 100, 2)
    if change > 0:
        mark = "↑"
    elif change < 0:
        mark = "↓"
        change = -change
    else:
        mark = "-"
    mesg = [
        "WTI유가원자재\n     ",
        str(last_value),
        "/",
        str(change),
        mark,
        "(",
        str(change_rate),
        "%",
        ")",
    ]
    mesg = " ".join(mesg)
    return mesg


if __name__ == "__main__":
    # print(get_exchange_rate())
    # print(get_dollar_index())
    # print(get_interest())
    # print(get_copper())
    # print(get_wti_oil())
    msg = (
        get_exchange_rate()
        + "\n"
        + get_dollar_index()
        + "\n"
        + get_interest()
        + "\n"
        + get_copper()
        + "\n"
        + get_wti_oil()
    )
    print(msg)
