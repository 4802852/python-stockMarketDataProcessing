import pandas as pd
import os


def get_krx():
    code_df = pd.read_html(
        "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13", header=0
    )[0]
    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    code_df.종목코드 = code_df.종목코드.map("{:06d}".format)
    # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
    code_df = code_df[["회사명", "종목코드"]]
    # 한글로된 컬럼명을 영어로 바꿔준다.
    code_df = code_df.rename(columns={"회사명": "name", "종목코드": "code"})
    return code_df


if __name__ == "__main__":
    df = get_krx()
    path = os.path.dirname(os.path.abspath(__file__))
    df.to_csv(path + "/krx.csv", index=False)
