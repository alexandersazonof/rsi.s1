import requests

def get_usdt_futures_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    symbols = [symbol['symbol'] for symbol in data['symbols'] if 'USDT' in symbol['symbol']]
    return symbols

usdt_futures_symbols = get_usdt_futures_symbols()
print(usdt_futures_symbols)
