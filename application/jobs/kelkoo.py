import json
import difflib
from fetchers import fetch_products_without_kelkoo
from fetchers import search_for_k_offer
from fetchers import fetch_exchange_rate
from dumpers import write_offers

# Does not work that well
# Try out the other library if time: https://stackoverflow.com/questions/6690739/fuzzy-string-comparison-in-python-confused-with-which-library-to-use
def get_highest_match_id(kelkoo_res, product_name) :
	highest_match = 0.0
	best_match = None
	for result in kelkoo_res :
		match = difflib.SequenceMatcher(None, product_name, result['Offer']['Title']).ratio()
		if match > highest_match :
			best_match = result['Offer']['Title']
			highest_match = match
	return best_match

def iterate_and_fetch_offers(products, country) :
	kelkoo_keys = json.load(open('application/config/api_keys.json'))['kelkoo'][country]
	found_offers = []
	offer_unique_cash = {}
	exchange_rate = fetch_exchange_rate(country)
	for i, product in enumerate(products) :
		try : 
				kelkoo_res = search_for_k_offer(kelkoo_keys, country, product['name'], product['price'])
		except Exception as e :
			print "There was an error with fetching offer data from Kelkoo: ", str(e)
			continue
		finally :
			# best_match = get_highest_match_id(kelkoo_res, product['name'])
			for result in kelkoo_res :

				# print json.dumps(result, indent=2)
				
				# Making sure all found offers are unique
				unique_str = str(product['id']) + result['Offer']['Title'] + result['Offer']['Merchant']['@id']
				if unique_str not in offer_unique_cash.itervalues() :
					found_offers.append([
						product['id'],
						'kelkoo_' + country,
						result['Offer']['Title'],
						result['Offer']['Merchant'].get('Name') or None,
						country,
						float(result['Offer']['Price']['Price']) * float(exchange_rate['rate']),
						None,
						None,
						result['Offer']['Url']
					])
				offer_unique_cash[unique_str] = unique_str
			write_offers(found_offers)

def sync_kelkoo_offers(country) :
	products_for_sync = fetch_products_without_kelkoo(country)
	iterate_and_fetch_offers(products_for_sync, country)
