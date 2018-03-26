# coding=utf-8
import json
import requests
import xmltodict
import time
import hashlib

def url_encode(string) :
	return "%20".join(string.split(" "))

def search_for_offer(api_keys, country, product_name, price) :
	try:
		req_url = sign_url(
			url_domain = str('http://{0}.shoppingapis.kelkoo.com' +
				'/V3/productSearch?query={1}&' +
				'sort=default_ranking&start=1&results=20&price_min={2}&show_products=1&show_subcategories=1&show_refinements=1&' +
				'aid={3}').format(
					country.lower(),
					url_encode(product_name),
					str(int(float(price) * 0.50)),
					api_keys['id']
				),
			key = api_keys['key']
		)
		res = requests.get(req_url)
		dict_res = xmltodict.parse(res.content)
	except Exception as e:
		print("There was an error when fetching product data from Kelkoo: ", e)
	finally :
		# print json.dumps(dict_res['ProductSearch']['Products']['Product'][:10], indent=2)
		return dict_res['ProductSearch']['Products']['Product'][:5]

def sign_url(url_domain, key) :
	# Creating a Unix timestamp for right now without milliseconds
	time_now = int(str(time.time()).split('.')[0])
	# Save the request URL with the time and key simply appended to the end
	req_url =  url_domain + "&timestamp=" + str(time_now) + str(key)
	# Get only the API url and strip away http://se.shoppingapis.kelkoo.com
	url_without_beginning = '/V3/' + req_url.split('/V3/')[1]
	# Hash string the url with md5
	m = hashlib.md5()
	m.update(url_without_beginning)
	# Base 64 encode it
	hash_url = m.digest().encode('base64').strip()
	# Replace characters that does not work in a url
	token = hash_url.replace('+', '.').replace('/', '_').replace('=', '-')
	# Return the whole request URL concat
	return url_domain + "&timestamp=" + str(time_now) + "&hash=" + token
