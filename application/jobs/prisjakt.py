from fetchers import get_products
from bs4 import BeautifulSoup
import re
from dumpers import write_products
from fetchers import fetch_products_without_prisjakt
from dumpers import write_prisjakt
from fetchers import fetch_prisjakt_products
from fetchers import fetch_prisjakt_product_offers
from dumpers import write_offers
from helpers import threaded_execution

# for idx, val in enumerate(ints):

def sync_products(category) :
	found_products = []
	try :
		products = get_products(category)
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
	write_products(found_products)

def iterate_and_fetch_products(wanted_products, country) :
	found_products = []
	try :
		fetched_products = get_products()
	except Exception as e :
		print "There was an error with scraping products from Prisjakt: ", str(e)
		return
	finally :
		for product in fetched_products :
			prod_name = product.select(".product-name a")[0].get_text()
			if prod_name in wanted_products :
				price = None
				if next(iter(product.select(".price") or []), None) is not None :
					price = int(''.join(re.findall(r'\d+', product.select(".price")[0].get_text())))
				found_products.append([
					wanted_products[prod_name],
					"https://www.prisjakt.nu" + product.select("a")[0].attrs["href"],
					country,
					price
				])
		write_prisjakt(found_products)

def iterate_and_fetch_offers(products, country) :
	found_offers = []
	for i, product in enumerate(products) :
		try :
			prisjakt_res = fetch_prisjakt_product_offers(product['url'], country)
		except Exception as e :
			print "There was an error with fetching offer data from Prisjakt: ", str(e)
			continue
		finally :
			# Maximum number of offers from the result that I want to store
			num_to_fetch = 30
			while num_to_fetch > 0 :
				try : 
					offer = prisjakt_res[30 - num_to_fetch]
					# Check so that we don't get offers on used products
					if offer.attrs['data-pris_typ'] == 'normal' :
						# Define empty variables
						retail_prod_name = ""
						retailer_name = ""
						price = None
						offer_url = ""
						# Do logical checks to see if the data exists
						if len(offer.select(".detailed2")) > 0 :
							retail_prod_name = offer.select(".detailed2")[0].get_text()
						if len(offer.select(".store-name-span")) > 0 :
							retailer_name = offer.select(".store-name-span")[0].get_text()
						if len(offer.select(".cell-bar a")) > 0 :
							price = int(''.join(re.findall(r'\d+', offer.select(".cell-bar a")[0].get_text())))
						if len(offer.select(".cell-bar a")) > 0 :
							offer_url = "https://www.prisjakt.nu" + offer.select(".cell-bar a")[0].attrs["href"]
						# Only write offers with complete data
						if retail_prod_name != "" and retailer_name != "" and price != None and offer_url != "" :
							found_offers.append([
								products[i]['product_id'],
								'prisjakt_' + country,
								retail_prod_name.strip(),
								retailer_name,
								country,
								price,
								None,
								None,
								offer_url
							])
					num_to_fetch -= 1
				# No more items exists
				except IndexError as e:
					num_to_fetch = 0
	write_offers(found_offers)

def sync_prisjakt_products(country) :
	products_for_sync = fetch_products_without_prisjakt(country)
	iterate_and_fetch_products(products_for_sync, country)

def sync_prisjakt_offers(country) :
	products_for_sync = fetch_prisjakt_products(country)
	threaded_execution(products_for_sync, iterate_and_fetch_offers, user_define_job=True, country=country)
