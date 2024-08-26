import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math

def get_data(start, end, symbols, column_name="Adj Close", include_spy=True, data_folder="./data"):
    dates = pd.date_range(start, end)
    df1 = pd.DataFrame(index=dates)
    df2 = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True, usecols=['Date', column_name])
    df2.rename(columns={column_name: "SPY"}, inplace=True)
    df1 = df1.join(df2, how='inner')
    for symbol in symbols:
        tmp_df = pd.read_csv(data_folder + '/'+ symbol + ".csv", index_col='Date', parse_dates=True, usecols=['Date', column_name])
        tmp_df.rename(columns={column_name: symbol}, inplace=True)
        df1 = df1.join(tmp_df, how='left', rsuffix='_'+symbol)
    if (not include_spy):
        df1.drop('SPY', axis=1, inplace=True)
    return df1

def simple_moving_average(data, window=20):
    return data.rolling(window=window).mean()


def bollinger_bands(data, window=9, num_std=2):
    sma = simple_moving_average(data, window=window)
    rolling_std = data.rolling(window=window).std()

    upper_band = sma + (rolling_std * num_std)
    lower_band = sma - (rolling_std * num_std)

    bollinger_band = sma

    result_df = pd.DataFrame({
        'Upper Band': upper_band,
        'Lower Band': lower_band,
        'Bollinger Band': bollinger_band
    }, index=data.index)  # Include the original index

    return result_df

def relative_strength_index(data):
    price_diff = data.diff(1)
    gain = price_diff.where(price_diff > 0, 0)
    loss = -price_diff.where(price_diff < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    # Initial RSI calculation (step one) using the first 14 days
    rs = avg_gain / avg_loss
    rsi_step_one = 100 - (100 / (1 + rs))

    # Smoothing step (step two)
    for i in range(14, len(rsi_step_one)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * 13 + gain.iloc[i]) / 14
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * 13 + loss.iloc[i]) / 14

    rs_smoothed = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs_smoothed))

    return rsi


def macd(data):
    df = data.copy()
    df['EMA-12'] = df['DIS'].ewm(12).mean()
    df['EMA-26'] = df['DIS'].ewm(26).mean()
    df['MACD'] = df['EMA-12'] - df['EMA-26']
    return df



def main():
    data = get_data('2018-01-01', '2019-12-31', ['DIS'])

    sma_data = simple_moving_average(data, window=20)
    plt.figure(figsize=(10, 6))
    plt.plot(data['DIS'], label='DIS Stock Price', color='blue')
    plt.plot(sma_data['DIS'], label='20-Day SMA', color='red')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('DIS Stock Price with 20-Day SMA')
    plt.legend()
    plt.show()

    bollinger_data = bollinger_bands(data['DIS'], window=9, num_std=2)  
    plt.figure(figsize=(10, 6))
    plt.plot(data['DIS'], label='DIS Stock Price', color='blue')
    plt.plot(bollinger_data['Bollinger Band'], label='Bollinger Band (9-Day SMA)', color='red')
    plt.plot(bollinger_data['Upper Band'], label='Upper Band', color='green', linestyle='--')
    plt.plot(bollinger_data['Lower Band'], label='Lower Band', color='orange', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('DIS Stock Price and Bollinger Bands')
    plt.legend()
    plt.show()

    rsi_data = relative_strength_index(data)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(rsi_data['DIS'], label='Relative Strength Index (RSI)', color='purple')
    ax1.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    ax1.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('RSI')
    ax1.set_title('RSI with Overbought and Oversold Lines')
    ax1.legend()
    ax2 = ax1.twinx()
    ax2.plot(data['DIS'], label='Stock Price', color='blue')
    ax2.set_ylabel('Stock Price', color='blue')
    ax2.legend(loc='upper right')
    plt.show()

    data = macd(data) # buy when macd goes positive
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(data['DIS'], label='DIS Stock Price', color='blue')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price', color='blue')
    ax1.tick_params('y', colors='blue')
    ax2 = ax1.twinx()
    ax2.plot(data['MACD'], label='MACD', color='red')
    ax2.set_ylabel('MACD', color='red')
    ax2.tick_params('y', colors='red')
    plt.title('DIS Stock Price with MACD')
    plt.show()



if __name__ == "__main__":
    main()
