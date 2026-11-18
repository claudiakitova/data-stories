# Can a Neural Network Predict Tomorrow's Bitcoin Price?

Price-forecasting tutorials often end with a chart where the predicted line hugs the real one. This project checks how much of that is real skill.

**Notebook:** [bitcoin_forecast.ipynb](bitcoin_forecast.ipynb) · **Data:** [btc_usdt_daily.csv](btc_usdt_daily.csv)

## Data

Daily Bitcoin prices in US dollars (BTC/USDT on Binance), January 2018 to October 2026: open, high, low, close, volume, and number of trades. 3,226 days, from Binance's public market data, so no account or key is needed.

## Approach

1. Charted the price and the last three months as candlesticks.
2. Split the daily trading volume into trend, weekly pattern, and remainder, and flagged days whose remainder was beyond 3 standard deviations.
3. Trained an LSTM neural network to predict the next day's change from the previous 30 days, on 2018–2023, and tested it on 2024 to October 2026. Compared it with the naive guess "tomorrow's price equals today's".

## Results

- Trading is lighter on weekends, about $0.9 billion below trend on Saturdays. Most unusual volume days are spikes on big price moves, such as +8.9% the day after the 2024 US election and −14% in February 2026.
- The LSTM was off by $1,357 a day on average; the naive guess, by $1,354. It called the direction right on 49.9% of days, while Bitcoin went up on 50.5% of them.
- A predicted-vs-actual price chart can't show forecasting skill: the naive guess looks just as good on it. A model needs to be compared with a simple baseline, on days it hasn't seen.

## Tools

Python, pandas, NumPy, statsmodels, TensorFlow / Keras (LSTM), matplotlib, mplfinance
