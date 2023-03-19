from datetime import datetime, timedelta

class MMath:
    # Simple Moving Average.
    # Parameters:
    # n = Number of days.
    # data = 2d array of CSGO market data.
    def sma(n, data):
        assert n*24+datetime.now().hour <= len(data), "N cannot be greater than the length of data collected. (21 * 24 + Current Hour of Day)"

        n = n*24+datetime.now().hour
        end = len(data)-n-1
        sum = 0
        for i in range(len(data)-1, end, -1):
            sum += float(data[i][1])
        return float(sum/n)