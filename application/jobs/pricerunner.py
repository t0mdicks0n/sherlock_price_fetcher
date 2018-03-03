from fetchers import fetch_products_without_pricerunner
from fetchers import fetch_product_id
from helpers import threaded_execution
from fetchers import fetch_product_id
from dumpers import write_pricerunner
import pprint

def iterate_and_fetch_products(products) :
	found_products = []
	try :
		for i, product in enumerate(products) :
			pricerunner_res = fetch_product_id(product['name'])
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

def sync_product_links() :
	products_for_sync = fetch_products_without_pricerunner()
	synced_products = threaded_execution(products_for_sync, iterate_and_fetch_products, user_define_job=True)
