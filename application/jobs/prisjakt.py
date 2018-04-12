from fetchers import get_products
from bs4 import BeautifulSoup
import re
from dumpers import write_products

def sync_prisjakt_products(category) :
	found_products = []
	try :
		products = get_products(category)
	except Exception as e :
		print "There was an error with scraping products from Prisjakt: ", str(e)
		return
	finally :
		for product in products :
			price = None
			if next(iter(product.select(".price") or []), None) is not None :
				price = int(''.join(re.findall(r'\d+', product.select(".price")[0].get_text())))
			found_products.append([
				product.select(".product-name a")[0].get_text(),
				category,
				product.select("img")[0].attrs["src"],
				price			
			])
	write_products(found_products)

# 'url': "https://www.prisjakt.nu" + product.select("a")[0].attrs["href"]