from fetchers import get_products
import re
from dumpers import write_products
from fetchers import fetch_categories

def filter_duplicate_products(found_products) :
	product_cache = {}
	unique_products = []
	for product in found_products :
		if product[0] not in product_cache :
			unique_products.append(product)
			product_cache[product[0]] = True
	return unique_products

def scrape_prisjakt_products(category, prisjakt_category_id) :
	found_products = []
	try :
		products = get_products(prisjakt_category_id)
	except Exception as e :
		print "There was an error with scraping products from Prisjakt: ", str(e)
		return
	finally :
		for idx, product in enumerate(products) :
			price = None
			# Sometime Prisjakt gray out the price for some this logic is adjusting for that
			if next(iter(product.select(".price") or []), None) is not None :
				price = int(''.join(re.findall(r'\d+', product.select(".price")[0].get_text())))
			else :
				price = int(''.join(re.findall(r'\d+', product.select(".muted a")[0].get_text())))
			# Scrape the rest of the data in the static structure
			found_products.append([
				product.select(".product-name a")[0].get_text(),
				category,
				product.select("a img")[0].attrs["src"],
				price,
				idx
			])
	found_products_unique = filter_duplicate_products(found_products)
	write_products(found_products_unique)

def iterate_over_categories_and_scrape(categories) :
	for category in categories :
		scrape_prisjakt_products(category['name'], category['prisjakt_category_id'])

def sync_products() :
	categories = fetch_categories()
	iterate_over_categories_and_scrape(categories)