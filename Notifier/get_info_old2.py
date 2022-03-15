import requests
import os

c_path = os.path.dirname(os.path.abspath(__file__))


def get_exchange_rate():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=650&pair_id_for_news=650&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/currencies/usd-krw",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    return ["USD/KRW", last_value]


def get_dollar_index():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8827&pair_id_for_news=8827&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/currencies/us-dollar-index",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    return ["$ Index", last_value]


def get_interest():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=23705&pair_id_for_news=23705&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    return ["US10Y", last_value]


def get_copper():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8831&pair_id_for_news=8831&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/commodities/copper",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    return ["구리", last_value]


def get_wti_oil():
    url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8849&pair_id_for_news=8849&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/commodities/crude-oil",
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    return ["WTI유가", last_value]


def get_message():
    p_data = []
    with open(c_path + "\last_info.txt", "r") as f:
        for _ in range(5):
            p_data.append(float(f.readline().strip()))
    name = [""] * 5
    c_data = [0] * 5
    name[0], c_data[0] = get_exchange_rate()
    name[1], c_data[1] = get_dollar_index()
    name[2], c_data[2] = get_interest()
    name[3], c_data[3] = get_copper()
    name[4], c_data[4] = get_wti_oil()
    with open(c_path + "\last_info.txt", "w") as f:
        for value in c_data:
            f.write(f"{value}\n")
    mesg = ""
    for i in range(len(name)):
        change = round(c_data[i] - p_data[i], 3)
        change_rate = round(change / p_data[i] * 100, 2)
        if change > 0:
            mark = "↑"
        elif change < 0:
            mark = "↓"
            change = -change
        else:
            mark = "-"
        tmp = [
            str(name[i]),
            "\n     ",
            str(c_data[i]),
            "/",
            str(change),
            mark,
            "(",
            str(change_rate),
            "%",
            ")",
        ]
        mesg += " ".join(tmp)
        if i != len(name) - 1:
            mesg += "\n"
    return mesg


if __name__ == "__main__":
    # print(get_exchange_rate())
    # print(get_dollar_index())
    # print(get_interest())
    # print(get_copper())
    # print(get_wti_oil())
    print(get_message())
