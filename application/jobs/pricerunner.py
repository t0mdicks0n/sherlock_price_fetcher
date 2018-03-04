from fetchers import fetch_products_without_pricerunner
from fetchers import fetch_pricerunner_products
from fetchers import fetch_product_id
from fetchers import fetch_product_offers
from helpers import threaded_execution
from fetchers import fetch_product_id
from dumpers import write_pricerunner
from dumpers import write_offers
import pprint

def iterate_and_fetch_products(products) :
	found_products = []
	try :
		for i, product in enumerate(products) :
			try : 
				pricerunner_res = fetch_product_id(product['name'])
			except Exception as e :
				continue		
			if len(pricerunner_res['products']) >= 1 :
				products[i]['url'] = pricerunner_res['products'][0].get('url') or None
				products[i]['lowest_price'] = pricerunner_res['products'][0].get('lowestPrice') or None
				found_products.append([products[i]['id'], products[i]['url'], products[i]['lowest_price']])
			elif len(pricerunner_res['suggestions']) >= 1 :
				products[i]['url'] = pricerunner_res['suggestions'][0].get('url') or None
				products[i]['lowest_price'] = pricerunner_res['suggestions'][0].get('lowestPrice') or None				
				found_products.append([products[i]['id'], products[i]['url'], products[i]['lowest_price']])
			else :
				found_products.append([products[i]['id'], None, None])
		del products
		# Write products to database
		write_pricerunner(found_products)
	except Exception as e :
		print("There was an error: ", e)

def iterate_and_fetch_offers(products) :
	found_offers = []
	try :
		for i, product in enumerate(products) :
			try : 
				pricerunner_res = fetch_product_offers(product['url'])
			except Exception as e :
				continue
			# Maximum number of products from the result that I want to store
			num_to_fetch = 4
			while num_to_fetch > 0 :
				try :
					offer = pricerunner_res[4 - num_to_fetch]
					found_offers.append([
						products[i]['product_id'],
						'pricerunner',
						offer['retailerProductName'],
						offer['retailer']['name'],
						offer.get('country') or None,
						int(offer['priceEx']['value'].split('.')[0]),
						int(offer['shippingCostFixEx'].split('.')[0]),
						True,
						products[i]['url'],
					])
					num_to_fetch -= 1
				except IndexError :
					# No more items exists
					num_to_fetch = 0
		del products
		write_offers(found_offers)
	except Exception as e :
		print("There was an error: ", e)

def sync_product_links() :
	products_for_sync = fetch_products_without_pricerunner()
	threaded_execution(products_for_sync, iterate_and_fetch_products, user_define_job=True)

def sync_pricerunner_offers () :
	products_for_sync = fetch_pricerunner_products()
	threaded_execution(products_for_sync, iterate_and_fetch_offers, user_define_job=True)

