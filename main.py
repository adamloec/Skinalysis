from market import Market
from mmath import MMath


if __name__ == "__main__":

    url = "https://steamcommunity.com/market/listings/730/Revolution%20Case"
    market = Market(url)
    market.scan()
    # for i in range(0, len(market.history)):
    #     print(market.history[i])
    print(MMath.sma(21, market.history))