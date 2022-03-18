import requests
import os

c_path = os.path.dirname(os.path.abspath(__file__))

data_list = {
    "USD/KRW": ["USD/KRW", 650, "https://www.investing.com/currencies/usd-krw"],
    "US10Y": ["US10Y", 23705, "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield"],
    "US2Y": ["US2Y", 23701, "https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield"],
    "COPPER": ["COPPER", 8831, "https://www.investing.com/commodities/copper"],
    "WTI_OIL": ["WTI_OIL", 8849, "https://www.investing.com/commodities/crude-oil"],
    "$_Index": ["$_Index", 8827, "https://www.investing.com/currencies/us-dollar-index"],
}


def get_data(data_name, pair_id, referer):
    url = f"https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id={pair_id}&pair_id_for_news={pair_id}&chart_type=area&pair_interval=900&candle_count=120&events=yes&volume_series=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": referer,
    }
    data = requests.get(url, headers=headers).json()
    last_value = float(data["attr"]["last_value"])
    return [data_name, last_value]


def get_message():
    series = ["USD/KRW", "US10Y", "US10Y-2Y", "COPPER", "WTI_OIL", "$_Index"]
    data_result = {}
    for na in data_list.keys():
        n, id, ref = data_list[na]
        nn, cd = get_data(n, id, ref)
        data_result[nn] = {"c_data": cd}
    data_result["US10Y-2Y"] = {
        "c_data": round(data_result["US10Y"]["c_data"] - data_result["US2Y"]["c_data"], 3)
    }
    try:
        with open(c_path + "\last_info.txt", "r") as f:
            for text in f:
                name, pd = map(str, text.split())
                data_result[name]["p_data"] = float(pd)
        data_result["US10Y-2Y"]["p_data"] = round(
            data_result["US10Y"]["p_data"] - data_result["US2Y"]["p_data"], 3
        )
    except:
        pass
    mesg = ""
    for i, name in enumerate(series):
        c_data = data_result[name]["c_data"]
        try:
            p_data = data_result[name]["p_data"]
        except:
            p_data = c_data
        change = round(c_data - p_data, 3)
        change_rate = round(change / p_data * 100, 2)
        if change > 0:
            mark = "↑"
        elif change < 0:
            mark = "↓"
            change = -change
        else:
            mark = "-"
        tmp = [
            str(name),
            "\n     ",
            str(c_data),
            "/",
            str(change),
            mark,
        ]
        if name != "US10Y-2Y":
            tmp += [
                "(",
                str(change_rate),
                "%",
                ")",
            ]
        mesg += " ".join(tmp)
        if i != len(name) - 1:
            mesg += "\n"
    with open(c_path + "\last_info.txt", "w") as f:
        for name in data_list.keys():
            value = data_result[name]["c_data"]
            f.write(f"{name} {value}\n")
    return mesg


if __name__ == "__main__":
    # print(get_exchange_rate())
    # print(get_dollar_index())
    # print(get_interest())
    # print(get_copper())
    # print(get_wti_oil())
    print(get_message())
