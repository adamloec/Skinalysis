from market import Market


if __name__ == "__main__":

    url = "https://steamcommunity.com/market/listings/730/Revolution%20Case"
    market = Market(url, 30)
    market.scan()

    for i in range(0, len(market.history)):
        print(market.history[i])