from fetchers import fetch_products_without_amazon
from fetchers import fetch_amazon_products
from fetchers import search_for_product
from fetchers import search_for_offer
from helpers import get_amazon_object
from dumpers import write_amazon
from dumpers import write_offers
from dumpers import del_empty_ama_res
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
				print "There was an error with fetching product data from Amazon: ", str(e)
				continue
			for result in amazon_res :
				found_products.append([
					product['id'],
					country,
					result['ASIN'],
					result['ItemAttributes'].get('Manufacturer') or None,
					result['ItemAttributes'].get('ProductGroup') or None,
					result['ItemAttributes'].get('Title') or None,
					result['DetailPageURL']
				])
		del products
		# Write products to database
		write_amazon(found_products)
	except Exception as e :
		print("There was an error: ", e)
		print products

def ama_result_iterator (amazon_res, exchange_rate) :
	fetched_data = []
	for res in amazon_res :
		try :
			fetched_data.append({
				'merchant_name' : res['Offers']['Offer']['Merchant']['Name'],
				'price' : amazon_value_to_sek(res['Offers']['Offer']['OfferListing']['Price']['Amount'], exchange_rate)
			})
		except Exception as e :
			fetched_data.append({
				'merchant_name' : None,
				'price' : None
			})
	return fetched_data

def ama_batch_fetcher(products, amazon, exchange_rate) :
	fetched_data = []
	asin_batcher = []
	for i, product in enumerate(products) :
		if i > 0 and i%10 == 0 :
			amazon_res = search_for_offer(','.join(asin_batcher), amazon)
			fetched_data = fetched_data + ama_result_iterator(amazon_res, exchange_rate)
			asin_batcher = []
		asin_batcher.append(product['asin_id'])
	amazon_res = search_for_offer(','.join(asin_batcher), amazon)
	fetched_data = fetched_data + ama_result_iterator(amazon_res, exchange_rate)
	# Temporary fix for amazon sometime returning empty results
	missing_res = len(products) - len(fetched_data)
	while missing_res > 0 :
		fetched_data.append({
			'merchant_name' : None,
			'price' : None
		})
		missing_res = len(products) - len(fetched_data)
	# Return the result
	return fetched_data

def iterate_and_fetch_offers(products, amazon, country) :
	found_offers = []
	offer_unique_cash = {}
	exchange_rate = fetch_exchange_rate(country)
	offer_data = ama_batch_fetcher(products, amazon, exchange_rate)
	try :
		for i, product in enumerate(products) :
			unique_str = str(product['product_id']) + str(offer_data[i]['merchant_name']) + product['product_name']
			if unique_str not in offer_unique_cash.itervalues() :		
				found_offers.append([
					product['product_id'],
					'amazon_' + country,
					product['product_name'],
					offer_data[i]['merchant_name'],
					country,
					offer_data[i]['price'],
					None,
					None,
					product['offer_url']
				])
			offer_unique_cash[unique_str] = unique_str
		write_offers(found_offers)
	except Exception as e :
		print("There was an error with fetching offers: ", e)

def sync_amazon_products(country) :
	products_for_sync = fetch_products_without_amazon(country)
	amazon = get_amazon_object(country)
	iterate_and_fetch_products(products_for_sync, amazon, country)

def sync_amazon_offers(country) :
	products_for_sync = fetch_amazon_products(country)
	amazon = get_amazon_object(country)
	iterate_and_fetch_offers(products_for_sync, amazon, country)
	# Delete amazon results which has no price (nothing to compare)
	del_empty_ama_res()