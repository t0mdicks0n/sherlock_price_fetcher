import requests
import json

def urlify(in_string) :
  return "%20".join(in_string.split())

def get_country_link() :
	return {
		'UK': {
			'fetch_id': 'https://www.pricerunner.com/public/search/suggest/uk?q=',
			'fetch_offers_1': 'https://www.pricerunner.com/public/v3/pl/',
			'fetch_offers_2': '/uk?urlName='
		},
		'SE': {
			'fetch_id': 'https://www.pricerunner.se/public/search/suggest/se?q=',
			'fetch_offers_1': 'https://www.pricerunner.se/public/v3/pl/',
			'fetch_offers_2': '/se?urlName='
		},
		'DK': {
			'fetch_id': 'https://www.pricerunner.dk/public/search/suggest/dk?q=',
			'fetch_offers_1': 'https://www.pricerunner.dk/public/v3/pl/',
			'fetch_offers_2': '/dk?urlName='
		}
	}

def fetch_product_id (product_name, country, retries=10) :
	headers = {
		'Content-Type': 'application/json;charset=utf-8',
		'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'authority': 'www.pricerunner.se'
	}
	# url = 'https://www.pricerunner.se/public/search/suggest/se?q=' + urlify(product_name)
	url = get_country_link()[country]['fetch_id'] + urlify(product_name)
	try :
		request = requests.get(url, headers=headers)
	except requests.exceptions.Timeout :
		print "Got a timeout on product " + product_name + " on Pricerunner."
		print request
		if retries < 10 :
			retries += 1
			fetch_product_id(product_name, retries)
	except requests.exceptions.RequestException as e :
		print "There was an error with getting product data for " + product_name + " on Pricerunner: " + str(e)
		raise e
	finally :
		res = request.json()
		return res

def fetch_product_offers(product_url, country, retries=10) :
	headers = {
		'Content-Type': 'application/json;charset=utf-8',
		'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'authority': 'www.pricerunner.se'
	}
	# Grab the link as we get it when matching the product and modify it according to the format pricerunner want
	url = get_country_link()[country]['fetch_offers_1'] + "1-" + product_url.split('/')[2].split('-')[1] + get_country_link()[country]['fetch_offers_2'] + '/'.join(product_url.split('/')[3:])
	try :
		request = requests.get(url, headers=headers)
	except requests.exceptions.Timeout :
		print "Got a timeout on product url " + product_url + " on Pricerunner."
		print request
		if retries < 10 :
			retries += 1
			fetch_product_offers(product_url, retries)
	except requests.exceptions.RequestException as e :
		print "There was an error with getting product offers for " + product_url + " on Pricerunner: " + str(e)
		raise e
	finally :
		# They have a 'internationalOffers' property as well with the same
		# offers array structure
		res = request.json()['nationalOffers']['offers']
		return res
