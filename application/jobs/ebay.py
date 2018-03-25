from fetchers import search_for_e_offer
from fetchers import fetch_products_without_ebay
from fetchers import fetch_exchange_rate
from dumpers import write_offers
import json

def iterate_and_fetch_offers(products, ebay_keys, country) :
	found_offers = []
	exchange_rate = fetch_exchange_rate(country)
	for i, product in enumerate(products) :
		try : 
			ebay_res = search_for_offer(ebay_keys, country, product['name'], product['price'])
		except Exception as e :
			continue
		finally :
			for result in ebay_res :
				found_offers.append([
					product['id'],
					'ebay_' + country,
					result['title'],
					None,
					country,
					float(result['sellingStatus']['currentPrice']['#text']) * float(exchange_rate['rate']),
					None,
					None,
					result['viewItemURL']
				])
	write_offers(found_offers)

def sync_ebay_offers(country) :
	products_for_sync = fetch_products_without_ebay(country)
	ebay_keys = json.load(open('application/config/api_keys.json'))['ebay']
	iterate_and_fetch_offers(products_for_sync, ebay_keys, country)
