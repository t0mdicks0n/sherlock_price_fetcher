from fetchers import fetch_products
from fetchers import search_for_product
from fetchers import search_for_offer
from helpers import get_amazon_object
from dumpers import write_amazon
import json

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
				amazon_res['ItemAttributes']['Manufacturer'],
				amazon_res['ItemAttributes']['ProductGroup'],
				amazon_res['ItemAttributes']['Title'],
				amazon_res['DetailPageURL']
			])
		del products
		# Write products to database
		write_amazon(found_products)
	except Exception as e :
		print("There was an error: ", e)

		print products

def sync_amazon_products(country) :
	products_for_sync = fetch_products(country)
	amazon = get_amazon_object(country)
	iterate_and_fetch_products(products_for_sync, amazon, country)

	# print json.dumps(search_for_product('Samsung Galaxy A5 2017 SM-A520F', amazon), indent=2, sort_keys=True)


def sync_amazon_offers() :
	products_for_sync = fetch_products()
	ama_keys = json.load(open('application/config/api_keys.json'))['amazon']
	amazon = bottlenose.Amazon(
		ama_keys['access_key'], ama_keys['secret_key'], ama_keys['associate_tag'],
		Region='UK', ErrorHandler=error_handler, MaxQPS=0.9,
		Parser=lambda text: xmltodict.parse(text)
	)
	print json.dumps(search_for_product('Motorola Moto G5 Plus (3GB RAM) 32GB', amazon), indent=2, sort_keys=True)
	# print json.dumps(amazon.ItemLookup(ItemId="B01MZCWGYB", ResponseGroup="Offers"), indent=2, sort_keys=True)
