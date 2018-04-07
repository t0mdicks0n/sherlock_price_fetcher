from fetchers import search_for_e_offer
from fetchers import fetch_products_without_ebay
from fetchers import fetch_exchange_rate
from dumpers import write_offers
from helpers import threaded_execution
import json

def iterate_and_fetch_offers(products, ebay_keys, country) :
	found_offers = []
	offer_unique_cash = {}
	exchange_rate = fetch_exchange_rate(country)
	for i, product in enumerate(products) :
		try : 
			ebay_res = search_for_e_offer(ebay_keys, country, product['name'], product['price'])
		except Exception as e :
			print "There was an error with fetching offer data from eBay: ", str(e)
			continue
		finally :
			for result in ebay_res :
				# Making sure all found offers are unique
				unique_str = str(product['id']) + result.get('title') or 'title' + result['sellerInfo'].get('sellerUserName') or 'sellerUserName' + result['viewItemURL']
				if unique_str not in offer_unique_cash.itervalues() :
					found_offers.append([
						product['id'],
						'ebay_' + country,
						result['title'],
						result['sellerInfo']['sellerUserName'],
						country,
						float(result['sellingStatus']['currentPrice']['#text']) * float(exchange_rate['rate']),
						None,
						None,
						result['viewItemURL']
					])
				offer_unique_cash[unique_str] = unique_str
	write_offers(found_offers)

def sync_ebay_offers(country) :
	products_for_sync = fetch_products_without_ebay(country)
	ebay_keys = json.load(open('application/config/api_keys.json'))['ebay']
	# iterate_and_fetch_offers(products_for_sync, ebay_keys, country)
	threaded_execution(products_for_sync, iterate_and_fetch_offers, user_define_job=True, country=country, ebay_keys=ebay_keys)
