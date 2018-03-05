from fetchers import fetch_products_without_amazon
from fetchers import fetch_amazon_products
from fetchers import search_for_product
from fetchers import search_for_offer
from helpers import get_amazon_object
from dumpers import write_amazon
from dumpers import write_offers
from helpers import amazon_value_to_sek
from fetchers import fetch_exchange_rate
import json
import sys
# UTF-8 bullshit
reload(sys)
sys.setdefaultencoding('utf-8')

def iterate_and_fetch_products(products, amazon, country) :
	found_products = []
	try :
		for i, product in enumerate(products) :
			try : 
				amazon_res = search_for_product(product['name'], amazon, product['price'])
			except Exception as e :
				continue
			found_products.append([
				product['id'],
				country,
				amazon_res['ASIN'],
				amazon_res['ItemAttributes'].get('Manufacturer') or None,
				amazon_res['ItemAttributes'].get('ProductGroup') or None,
				amazon_res['ItemAttributes'].get('Title') or None,
				amazon_res['DetailPageURL']
			])
		del products
		# Write products to database
		write_amazon(found_products)
	except Exception as e :
		print("There was an error: ", e)
		print products

def iterate_and_fetch_offers(products, amazon, country) :
	found_offers = []
	exchange_rate = fetch_exchange_rate(country)
	try :
		for i, product in enumerate(products) :
			amazon_res = search_for_offer(product['asin_id'], amazon)
			found_offers.append([
				product['product_id'],
				'amazon',
				product['product_name'],
				'amazon_' + country,
				country,
				amazon_value_to_sek(amazon_res['OfferListing']['Price']['Amount'], exchange_rate),
				None,
				None,
				product['offer_url']
			])
		write_offers(found_offers)
	except Exception as e :
		print("There was an error: ", e)

def sync_amazon_products(country) :
	products_for_sync = fetch_products_without_amazon(country)
	amazon = get_amazon_object(country)
	iterate_and_fetch_products(products_for_sync, amazon, country)

def sync_amazon_offers(country) :
	products_for_sync = fetch_amazon_products()
	amazon = get_amazon_object(country)
	iterate_and_fetch_offers(products_for_sync, amazon, country)
