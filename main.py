import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR-STOCK-API-KEY"
NEWS_API_KEY = "YOUR-NEWS-API-KEY"

account_sid = "YOUR-ACCOUNT-SIDE"
auth_token = "YOUR-AUTH-TOKEN"


STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

stock_response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

stock_yday = float(data_list[0]["4. close"])
stock_dbyday = float(data_list[1]["4. close"])

difference = abs(stock_yday - stock_dbyday)
percentage_difference = round(difference / stock_dbyday * 100, 2)

def diference_direction():
    if stock_dbyday > stock_yday:
        return "📉"
    elif stock_dbyday < stock_yday:
        return "📈"

if percentage_difference >= 5:
    NEWS_PARAMETERS = {
        "apiKey": NEWS_API_KEY,
        "q": "Tesla",
        "sortBy": "publishedAt"
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    news_data = news_response.json()["articles"]

    top_3 = news_data[:3]

    title_1 = top_3[0]["title"]
    description_1 = top_3[0]["description"]
    title_2 = top_3[1]["title"]
    description_2 = top_3[1]["description"]
    title_3 = top_3[2]["title"]
    description_3 = top_3[2]["description"]
    news_list = [(title_1, description_1), (title_2, description_2), (title_3, description_3)]


    def diference_direction():
        if stock_dbyday > stock_yday:
            return "📉"
        elif stock_dbyday < stock_yday:
            return "📈"


    for num in range(0, 3):
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body= f"TSLA: {diference_direction()}{percentage_difference}% "
                  f"Headline: {news_list[num][0]} "
                  f"Brief: {news_list[num][1]}",
            from_="+19895026250",
            to="+34692448752"
        )
        print(message.status)


