from fetchers import get_products
from bs4 import BeautifulSoup
import re

def sync_prisjakt_products(category) :
	products = get_products()
	for product in products :
		price = None
		if next(iter(product.select(".price") or []), None) is not None :
			price = int(''.join(re.findall(r'\d+', product.select(".price")[0].get_text())))
		print {
			'Product Name': product.select(".product-name a")[0].get_text(),
			'Price': price,
			'Img': product.select("img")[0].attrs["src"],
			'category': category,
			
		}
