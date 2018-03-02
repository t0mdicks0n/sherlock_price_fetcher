import requests
import json

def urlify(in_string) :
  return "%20".join(in_string.split())

def fetch_product_id (product_name, retries=10) :
	headers = {
		'Content-Type': 'application/json;charset=utf-8',
		'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'authority': 'www.pricerunner.se'
	}
	url = 'https://www.pricerunner.se/public/search/suggest/se?q=' + urlify(product_name)
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
