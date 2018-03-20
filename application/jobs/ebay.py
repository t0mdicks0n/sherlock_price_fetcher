from fetchers import search_for_offer
import json

def sync_ebay_offers(country, product_name) :
	ebay_keys = json.load(open('application/config/api_keys.json'))['ebay']
	search_for_offer(ebay_keys, country, product_name)