# Demo cbpro-portfolio-tracker
import numpy as np
import pandas as pd
import datetime

# Coinbase Pro portfolio tracker:
import cbpro.portfolio
import cbpro.markets
import cbpro._api

# API:
api_key_file = "rangel-default-portfolio.secret"
api = cbpro._api.apiwrapper(api_key_file)
myportfolio = cbpro.portfolio.portfolio(api_key_file)
markets = cbpro.markets.markets(api_key_file)

# account holdings:
holdings = myportfolio.holdings()

# cbpro markets:
usd_products = markets.usd_products()
stablecoin_products = markets.stablecoin_products()

# markets price history:
start = datetime.datetime.strptime("2020-01-01","%Y-%m-%d")
end = datetime.datetime.today()
btc = markets.price_history(
	"BTC-USD",
	start=start,
	end=end,
	granularity=86400,
	)
btc.to_excel("~/Desktop/btc-prices.xlsx")

# get account ledger:
#ledger = myportfolio.ledger()
#ledger.to_excel("~/Desktop/ledger.xlsx")
