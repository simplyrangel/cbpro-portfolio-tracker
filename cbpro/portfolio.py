import numpy as np
import pandas as pd
import datetime

# internal functions:
import cbpro._utils as utils
from cbpro._api import apiwrapper

# Pandas index slice:
idx = pd.IndexSlice

class portfolio(apiwrapper):
	def __init__(self,api_key_file):
		apiwrapper.__init__(self,api_key_file)
		
	def holdings(self):
		api_output = self.query("/accounts")
		df = pd.DataFrame(api_output)
		for col in ["balance","hold","available"]:
			df.loc[:,col] = df[col].astype(np.float)
		return df.sort_values(
			by="balance",
			ascending=False,
			).set_index("currency"
			)
		
	def ledger(self):
		df = self.holdings()
		frames = []
		for coin in df.index:
			coin_id = df.loc[coin,"id"]
			api_output = self.query("/accounts/%s/ledger"%coin_id)
			coin_ledger = utils.ledger2df(api_output)
			frames.append(coin_ledger)
		mdf = pd.concat(
			frames,
			keys=list(df.index),
			names=["coin","transaction_no"],
			)
		return utils.update_ledger(mdf)
		
	def daily_history(self,ledger=None):
		if ledger is None:
			ledger = self.ledger()
		coins_in_ledger = ledger.index.levels[0].tolist()
		
		# create dataframe based on ledger contents:
		date_range = pd.date_range(
			start=ledger.index.levels[1].min().date(),
			end=datetime.datetime.today(),
			freq="D",
			tz=None,
			)
		mdf = pd.DataFrame(
			np.nan,
			index=date_range,
			columns=coins_in_ledger,
			)
		
		# add each coin's contents and return populated
		# multiindex dataframe:
		for coin in coins_in_ledger:
			df = ledger.loc[idx[coin,:],:]
			df = df.reset_index().set_index("created_at")
			df = df.resample("D").last().dropna(how="all")
			mdf.loc[df.index,coin] = df.balance
		return mdf.ffill().fillna(0.0)






