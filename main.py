from market import Market


if __name__ == "__main__":

    url = "https://steamcommunity.com/market/listings/730/Revolution%20Case"
    market = Market(url, 1)
    market.scan()
    print(market.sma())