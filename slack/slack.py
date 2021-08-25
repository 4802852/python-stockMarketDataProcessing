import requests
import json
import os

path = os.path.dirname(os.path.abspath(__file__))


def post_message(token, channel, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        data={"token": token, "channel": channel, "text": text},
    )
    if response.status_code == 200:
        print("sucessfully sent!")
    else:
        print("message fails..")


def to_slack(text, to_channel="#stock"):
    if to_channel == "#exchange-rate":
        channel = "#exchange-rate"
    else:
        channel = "#stock"
    try:
        secret_file = path + "\secrets.json"
        with open(secret_file) as f:
            secrets = json.loads(f.read())
        myToken = secrets["Token"]
        post_message(myToken, channel, text)
    except:
        print("No secret key!")
        print(text)


# to_slack("hello! everybody")
