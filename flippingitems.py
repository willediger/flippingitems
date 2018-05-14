import requests
import json
import os

__author__ = "Will Ediger"

use_live_data = False
base_osb_url = 'https://rsbuddy.com/exchange/summary.json'
current_price_osb_url = 'https://api.rsbuddy.com/grandExchange?a=guidePrice&i={osb_id}'
historic_prices_osb_url = 'https://api.rsbuddy.com/grandExchange?a=graph&g={min_between_price}&start={start_time}&i={osb_id}'


class RsItem(object):
	def __init__(self, osb_id, name):
		self.osb_id = osb_id
		self.name = name
		self.buying_price = 0
		self.selling_price = 0
		self.overall_price = 0
		self.buying_qty = 0
		self.selling_qty = 0
		self.historic_prices = []

	def __repr__(self):
		return '<RsItem osb_id:{0}, name:{1}, buying_price: {2}, selling_price: {3}, overall_price: {4}, buying_qty: {5}, selling_qty: {6}, historic_prices: {7}>'\
			.format(self.osb_id, self.name, self.buying_price, self.selling_price, self.overall_price, self.buying_qty, self.selling_qty, self.historic_prices)


def parse_json():
	if use_live_data:
		json_str = requests.get(base_osb_url).content.decode('utf-8')
	else:
		json_str = open(os.path.join('osbuddy_cached', 'summary.json'), 'r').read()

	summary = json.loads(json_str)

	items = []

	for k1, v1 in summary.items():
		if isinstance(v1, dict):
			rs_item = RsItem(v1['id'], v1['name'])
			if use_live_data:
				latest_prices_json = requests.get(current_price_osb_url.format(osb_id=rs_item.osb_id)).content.decode(
					'utf-8')
			else:
				latest_filename = 'latest{osb_id}.json'.format(osb_id=rs_item.osb_id)
				latest_prices_json = open(os.path.join('osbuddy_cached', latest_filename), 'r').read()

			current_prices = json.loads(latest_prices_json)
			rs_item.buying_price = current_prices['buying']
			rs_item.selling_price = current_prices['selling']
			rs_item.buying_qty = current_prices['buyingQuantity']
			rs_item.selling_qty = current_prices['sellingQuantity']
			rs_item.overall_price = current_prices['overall']
			items.append(rs_item)

	return items


items = parse_json()
print(items)
