import pandas as pd
import requests
import re
import os
from random import random
import time
import traceback


def get_data(ticker):
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(ticker)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    }
    html = requests.get(url, headers=headers).text
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=Y&encparam={}&id={}".format(
        ticker, encparam, encid
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Referer": "HACK",
    }
    html = requests.get(url, headers=headers).text

    data = pd.read_html(html)[1]
    column_name_old = data.columns
    column_name = []
    for i in range(len(column_name_old)):
        column_name.append(column_name_old[i][1].strip())
    data.columns = column_name
    data.set_index("주요재무정보", inplace=True)
    data = data.loc[["매출액", "영업이익", "ROE(%)", "현금DPS(원)", "현금배당수익률"]]
    column_name_old = data.columns
    column_name = []
    for i in range(len(column_name_old)):
        column_name.append(column_name_old[i].split("/")[0])
    data.columns = column_name
    return data


def csv_open(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(path + "/" + filename, converters={i: str for i in range(100)})
    return df


def checker(df):
    for i in range(len(df)):
        print("Getting {} Information...".format(df.loc[i, "name"]))
        try:
            tmp_data = get_data(df.loc[i, "code"])
            columns = tmp_data.columns
            # 매출액 증가 checker
            revenue_grow = True
            revenue_old = 0
            revenue_averager = []
            for j in range(5):
                revenue = tmp_data.loc["매출액", columns[j]]
                revenue_averager.append(revenue)
                df.loc[i, f"매출 {j}"] = revenue
                if revenue < revenue_old:
                    revenue_grow = False
                revenue_old = revenue
            if revenue_grow:
                df.loc[i, "매출 증가 Check"] = revenue_grow
            else:
                average = sum(revenue_averager) / len(revenue_averager)
                if average <= revenue:
                    df.loc[i, "매출 증가 Check"] = "CHECK"
                else:
                    df.loc[i, "매출 증가 Check"] = False
            # 흑자 기업 checker
            earning_grow = True
            earning_positive = True
            earning_old = 0
            earning_averager = []
            for j in range(5):
                earning = tmp_data.loc["영업이익", columns[j]]
                earning_averager.append(earning)
                df.loc[i, f"영업이익 {j}"] = earning
                if earning <= 0:
                    earning_positive = False
                if earning < earning_old:
                    earning_grow = False
                earning_old = earning
            df.loc[i, "영업이익 Check"] = earning_positive
            if earning_grow:
                df.loc[i, "영업이익 증가 Check"] = earning_grow
            else:
                average = sum(earning_averager) / len(earning_averager)
                if average <= earning:
                    df.loc[i, "영업이익 증가 Check"] = "CHECK"
                else:
                    df.loc[i, "영업이익 증가 Check"] = earning_grow
            # ROE checker
            roe = []
            for j in range(5):
                roe_tmp = tmp_data.loc["ROE(%)", columns[j]]
                if roe_tmp == roe_tmp:
                    roe.append(roe_tmp)
                df.loc[i, f"ROE {j}"] = roe_tmp
            roe_average = round(sum(roe) / len(roe), 2)
            if roe_average >= 10:
                df.loc[i, "ROE 평균 check"] = True
            else:
                df.loc[i, "ROE 평균 check"] = False
            # 현금 배당률 증가 checker
            dividend_grow = True
            dividend_old = 0
            for j in range(5):
                dividend = tmp_data.loc["현금DPS(원)", columns[j]]
                df.loc[i, f"배당금 {j}"] = dividend
                if dividend == 0:
                    dividend_grow = False
                if dividend < dividend_old:
                    dividend_grow = False
                dividend_old = dividend
            df.loc[i, "배당금증가 Check"] = dividend_grow
            # 배당수익률 checker
            df.loc[i, "현금배당수익률"] = tmp_data.loc["현금배당수익률", columns[4]]
            if df.loc[i, "현금배당수익률"] >= 1:
                df.loc[i, "배당 checker"] = True
            else:
                df.loc[i, "배당 checker"] = False
        except Exception:
            err = traceback.format_exc()
            df.loc[i, "error code"] = "ERROR"
        # random sleeper
        rand_value = random() * 2 + 1
        time.sleep(rand_value)
    return df


def save_csv(df, filename):
    path = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(path + "/" + filename)


def main():
    filename = "krx.csv"
    df = csv_open(filename)
    df = checker(df)
    output_name = "checker.csv"
    save_csv(df, output_name)


if __name__ == "__main__":
    main()
