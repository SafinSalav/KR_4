import json
import os
import requests

API_KEY = os.getenv('API_key')


def get_currency_rate(currency):
    if currency == 'BYR':
        currency = 'BYN'
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={'apikey': API_KEY})
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


