import requests
from bs4 import BeautifulSoup

def scrape_prod_site(prod_count) :
	try : 
		request_string = str("https://www.prisjakt.nu/kategori.php?k=103") + "&s=" + str(prod_count)
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
			'Cookie': "usersettings=%7B%22sidebar_layout_mode%22%3A%22hidden%22%2C%22active_sidebar_list%22%3A%22MyLists%22%2C%22filter_layout_mode%22%3A%22maximized%22%2C%22category_matrix_layout%22%3A%22img%22%2C%22category_realtime_search%22%3A%221%22%2C%22category_nav_layout%22%3A%22list%22%2C%22products_per_page%22%3A%22100%22%2C%22products_per_page_mixed%22%3A1000%2C%22products_per_page_image%22%3A1000%2C%22mobile_products_per_page%22%3A%2250%22%2C%22mobile_products_per_page_mixed%22%3A%2250%22%2C%22mobile_products_per_page_image%22%3A%2230%22%7D"
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		print 'Status Code: ', page.status_code
	except Exception as e:
		print("There was an error when scraping product data from Prisjakt: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		return soup.select("#prodlista #div_produktlista .drg-sidebar")

def get_products(products=[], prod_count=0) :
	print "prod_count", str(prod_count)
	fetched_products = scrape_prod_site(prod_count)
	if len(fetched_products) == 0 :
		print "Done! Fetched ", str(len(products)), " number of products!"
		return products
	else :
		new_products = products + fetched_products
		prod_count = prod_count + len(fetched_products)
		return get_products(new_products, prod_count)
