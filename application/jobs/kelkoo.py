import json
from fetchers import fetch_products_without_kelkoo
from fetchers import search_for_k_offer
from fetchers import fetch_exchange_rate
from dumpers import write_offers

def iterate_and_fetch_offers(products, country) :
	kelkoo_keys = json.load(open('application/config/api_keys.json'))['kelkoo'][country]
	found_offers = []
	exchange_rate = fetch_exchange_rate(country)
	for i, product in enumerate(products) :
		try : 
				kelkoo_res = search_for_k_offer(kelkoo_keys, country, product['name'], product['price'])
		except Exception as e :
			print "There was an error with fetching offer data from Kelkoo: ", str(e)
			continue
		finally :
			for result in kelkoo_res :
				found_offers.append([
					product['id'],
					'kelkoo_' + country,
					result['Offer']['Title'],
					result['Offer']['Merchant']['Name'],
					country,
					float(result['Offer']['Price']['Price']) * float(exchange_rate['rate']),
					None,
					None,
					result['Offer']['Url']
				])
			write_offers(found_offers)

def sync_kelkoo_offers(country) :
	products_for_sync = fetch_products_without_kelkoo(country)
	iterate_and_fetch_offers(products_for_sync, country)
