from fetchers import fetch_products_without_pricerunner
from fetchers import fetch_product_id
import pprint

def sync_product_links() :
	products_for_sync = fetch_products_without_pricerunner()
	
	# print fetch_product_id('Meizu M3 Note 32GB')

