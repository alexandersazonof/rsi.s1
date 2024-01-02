import aiohttp
import asyncio
import pandas as pd
from ta.momentum import RSIIndicator
import ast

async def get_futures_data(session, symbol, interval, limit=200):
    url = f"https://fapi.binance.com/fapi/v1/klines"
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    async with session.get(url, params=params) as response:
        data = await response.json()
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        return df

def calculate_rsi(df, period=14):
    rsi_indicator = RSIIndicator(df['close'], period)
    df['RSI'] = rsi_indicator.rsi()
    return df

async def monitor_rsi(session, symbol):
    while True:
        data = await get_futures_data(session, symbol, '5m')
        data_with_rsi = calculate_rsi(data)

        if not data_with_rsi.empty:
            current_rsi = data_with_rsi['RSI'].iloc[-1]
        else:
            current_rsi = 0

        if current_rsi == 0 or current_rsi == 100:
            await asyncio.sleep(10)
            continue
        if current_rsi > 70:
            print(f"Symbol: {symbol}, Current RSI: {current_rsi} (Overbought)")
        elif current_rsi < 30:
            print(f"Symbol: {symbol}, Current RSI: {current_rsi} (Oversold)")

        await asyncio.sleep(60)

async def main():
    file_path = 'data/symbols_v2.txt'
    with open(file_path, 'r') as file:
        symbols_str = file.read()
        symbols = ast.literal_eval(symbols_str)

    async with aiohttp.ClientSession() as session:
        tasks = [monitor_rsi(session, symbol) for symbol in symbols]
        await asyncio.gather(*tasks)

try:
    print('-----------------START SCRIPT-----------------')
    asyncio.run(main())
except Exception as e:
    print(f"Error: {e}")