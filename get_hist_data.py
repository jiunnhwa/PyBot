import config, csv
from binance.client import Client
from datetime import date, timedelta

client = Client(config.API_KEY, config.API_SECRET)

EndDate = date.today()
StartDate = EndDate - timedelta(days=10)
# print("Today's date:", EndDate.strftime("%d %b, %Y"),  StartDate.strftime("%d %b, %Y"))
CCY = "BTCUSDT"
TF = "M15"
fname = f'{CCY}_{TF}.csv'

# fetch 1 minute klines for the last day up until now
candlesticks = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

# fetch StartDate till EndDate
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, StartDate.strftime("%d %b, %Y"), EndDate.strftime("%d %b, %Y"))
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2020", "12 Jul, 2020")
#candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017", "12 Jul, 2020")


csvfile = open(f'./data/{fname}', 'w', newline='') 
candlestick_writer = csv.writer(csvfile, delimiter=',')

for candlestick in  candlesticks:
    # print(candlestick)
    candlestick[0] = candlestick[0] / 1000  #de-millisec
    candlestick_writer.writerow(candlestick)
csvfile.close()
