from fetchers import fetch_products_without_pricerunner
from fetchers import fetch_pricerunner_products
from fetchers import fetch_product_id
from fetchers import fetch_product_offers
from helpers import threaded_execution
from fetchers import fetch_product_id
from fetchers import fetch_exchange_rate
from dumpers import write_pricerunner
from dumpers import write_offers
from helpers import print_exception
import pprint
import json

def iterate_and_fetch_products(products, country) :
	found_products = []
	try :
		for i, product in enumerate(products) :
			try : 
				pricerunner_res = fetch_product_id(product['name'], country)
			except Exception as e :
				print "There was an error with fetching product data from Pricerunner: ", str(e)
				continue
			if len(pricerunner_res.get('products') or []) >= 1 :
				products[i]['url'] = pricerunner_res['products'][0].get('url') or None
				products[i]['lowest_price'] = pricerunner_res['products'][0].get('lowestPrice') or None
				found_products.append([
					country,
					products[i]['id'],
					products[i]['url'],
					float(products[i]['lowest_price']['amount'])
				])
			elif len(pricerunner_res.get('suggestions') or []) >= 1 :
				products[i]['url'] = pricerunner_res['suggestions'][0].get('url') or None
				products[i]['lowest_price'] = pricerunner_res['suggestions'][0].get('lowestPrice') or None
				found_products.append([
					country,
					products[i]['id'],
					products[i]['url'],
					None if (products[i]['lowest_price'] is None) else float(products[i]['lowest_price']['amount'])
				])
			else :
				found_products.append([
					country,
					products[i]['id'],
					None,
					None
				])
		del products
		# Write products to database
		write_pricerunner(found_products)
	except Exception as e :
		print_exception(caller="iterate_and_fetch_products", exception=e)

def iterate_and_fetch_offers(products, country) :
	found_offers = []
	exchange_rate = fetch_exchange_rate(country)
	try :
		for i, product in enumerate(products) :
			try : 
				pricerunner_res = fetch_product_offers(product['url'], country)
			except Exception as e :
				print "There was an error with fetching offer data from Pricerunner: ", str(e)
				continue
			# Maximum number of products from the result that I want to store
			num_to_fetch = 15
			while num_to_fetch > 0 :
				try :
					offer = pricerunner_res[15 - num_to_fetch]
					if offer.get('retailerInfoUrl', None) is not None :
						if offer.get('price', None) is not None :
							found_offers.append([
								products[i]['product_id'],
								'pricerunner_' + country,
								offer['productName'],
								offer['retailerName'],
								country,
								float(offer['price']) * float(exchange_rate['rate']),
								# float(offer['shipping'].split('.')[0]) * float(exchange_rate['rate']),
								None,
								True,
								'https://www.pricerunner.' + (country.lower() if country != 'UK' else 'com') + offer['retailerClickout']
							])
					num_to_fetch -= 1
				except IndexError :
					# No more items exists
					num_to_fetch = 0
		del products
		write_offers(found_offers)
	except Exception as e :
		print_exception(caller="iterate_and_fetch_offers", exception=e)

def sync_product_links(country) :
	products_for_sync = fetch_products_without_pricerunner(country)
	threaded_execution(products_for_sync, iterate_and_fetch_products, user_define_job=True, country=country)

def sync_pricerunner_offers(country) :
	products_for_sync = fetch_pricerunner_products(country)
	threaded_execution(products_for_sync, iterate_and_fetch_offers, user_define_job=True, country=country)
