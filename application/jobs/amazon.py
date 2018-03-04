from fetchers import fetch_products
from fetchers import search_for_offer
import json
import bottlenose
import xmltodict
import random
import time
from urllib2 import HTTPError

def error_handler(err):
	ex = err['exception']
	if isinstance(ex, HTTPError) and ex.code == 503:
		time.sleep(random.expovariate(0.1))
		return True

def sync_amazon_offers () :
	products_for_sync = fetch_products()
	ama_keys = json.load(open('application/config/api_keys.json'))['amazon']
	amazon = bottlenose.Amazon(
		ama_keys['access_key'], ama_keys['secret_key'], ama_keys['associate_tag'],
		Region='UK', ErrorHandler=error_handler, MaxQPS=0.9,
		Parser=lambda text: xmltodict.parse(text)
	)
	
	print json.dumps(search_for_offer('Motorola Moto G5 Plus (3GB RAM) 32GB', amazon), indent=2, sort_keys=True)
	# print json.dumps(amazon.ItemLookup(ItemId="B0754KCNVQ", ResponseGroup="Offers"), indent=2, sort_keys=True)
