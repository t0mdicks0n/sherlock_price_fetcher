import requests
from bs4 import BeautifulSoup

def scrape_prod_site(prod_count, prisjakt_category_id) :
	try : 
		request_string = "https://classic.prisjakt.nu/kategori.php?k=" + prisjakt_category_id + "&s=" + str(prod_count)
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
			'Cookie': "usersettings=%7B%22sidebar_layout_mode%22%3A%22hidden%22%2C%22active_sidebar_list%22%3A%22MyLists%22%2C%22filter_layout_mode%22%3A%22maximized%22%2C%22category_matrix_layout%22%3A%22img%22%2C%22category_realtime_search%22%3A%221%22%2C%22category_nav_layout%22%3A%22list%22%2C%22products_per_page%22%3A%22100%22%2C%22products_per_page_mixed%22%3A1000%2C%22products_per_page_image%22%3A1000%2C%22mobile_products_per_page%22%3A%2250%22%2C%22mobile_products_per_page_mixed%22%3A%2250%22%2C%22mobile_products_per_page_image%22%3A%2230%22%7D"
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		if page.status_code != 200 :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when scraping product data from Prisjakt: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		'''
			So right now we are scraping data from the classis view of Prisjakt. Early 2019 they changed the site somewhat.
			It's still a old PHP web app that probably will work just as fine to scrape easily but the classes, ids and
			structures are all changed. Below is a start of the soup query to scrape product data from the new site.
			Remember that when doing this I will want to remove the "classic" in https://classic.prisjakt.nu/
		'''
		# return soup.select(
		# 	"""
		# 		body #root .app .app--main .category-page 
		# 		.page-content .page-content--wrapper 
		# 		.page-content--content .category-page--wrapper 
		# 		.category-page--gutter .category-page--product-wrapper 
		# 		.category-page--products section .pj-ui-panel 
		# 		.pj-ui-panel--grid .pj-ui-product-listing 
		# 		div[class='pj-ui-product-listing--item pj-ui-product-listing--item-grid']
		# 	"""
		# )
		return soup.select("#prodlista #div_produktlista .drg-sidebar")

# TODO: When category=False we want to fetch data for all different available categories
def get_products(prisjakt_category_id, products=[], prod_count=0) :
	print "prod_count", str(prod_count), " for prisjakt_category_id ", str(prisjakt_category_id)
	fetched_products = scrape_prod_site(prod_count, prisjakt_category_id)
	if len(fetched_products) == 0 :
		print "Done! Fetched ", str(len(products)), " number of products for the prisjakt_category_id " + prisjakt_category_id + "!"
		return products
	else :
		new_products = products + fetched_products
		prod_count = prod_count + len(fetched_products)
		return get_products(prisjakt_category_id, new_products, prod_count)

def fetch_prisjakt_product_offers(url, country) :
	try : 

		# Adjust the url to go on the classiv version of Prisjakts web. See discussion in code above
		request_string = url.split("www")[0] + "classic" + url.split("www")[1] + "&hide=used%2Cdemo"
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		if page.status_code != 200 :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when scraping a offer site from Prisjakt: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		return soup.select(".v-centered")
		# return soup.find_all('tr', class_='v-centered')
