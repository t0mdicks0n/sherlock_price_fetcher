import json
import requests
from bs4 import BeautifulSoup

def format_price(price) :
	return format(price, '.2f').replace('.', '')

def search_for_product(product_name, amazon, price) :
	try : 
		response = amazon.ItemSearch(
			Keywords=product_name,
			SearchIndex="All",
			Condition="New",
			# Provide a minimum price for better results
			MinimumPrice=format_price(price * 0.85)
		)
	except Exception as e:
		print "There was an error when calling the Amazon API: ", e
	finally :
		# print json.dumps(response, indent=2, sort_keys=True)
		# Grab up to 7 responses
		return response['ItemSearchResponse']['Items']['Item'][:7]

def search_for_offer(asin, amazon) :
	try :
		response = amazon.ItemLookup(
			ItemId=asin,
			ResponseGroup="OfferFull",
			IdType="ASIN",
			Condition="New",
			# MerchantId="Amazon"
		)
	except Exception as e:
		print "There was an error when calling the Amazon API: ", e
	finally :
		# print json.dumps(response, indent=2, sort_keys=True)
		# print json.dumps(response['ItemLookupResponse']['Items']['Item'], indent=2, sort_keys=True)
		return response['ItemLookupResponse']['Items']['Item']

def get_country_url (country) :
	if country == 'UK' :
		return 'https://www.amazon.co.uk'
	elif country == 'DE' :
		return 'https://www.amazon.de'
	elif country == 'IT' :
		return 'https://www.amazon.it'
	elif country == 'ES' :
		return 'https://www.amazon.es'
	else :
		print "Country URL is not specified!"

def fetch_amazon_price(asin, country) :
	try : 
		request_string = get_country_url(country) + '/dp/' + asin
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		if page.status_code != 200 :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when scraping a offer site from Amazon: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		print soup.select("#rightCol #desktop_buybox #buybox span")[0].get_text()
		return soup.select("#rightCol #desktop_buybox #buybox span")[0].get_text()
