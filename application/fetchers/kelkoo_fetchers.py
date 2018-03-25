# coding=utf-8
import json
import requests
import xmltodict

# Kelkoo bullshit
import time
import hashlib

def url_encode(string) :
	return "%20".join(string.split(" "))

def search_for_offer() :
	req_url = sign_url('http://se.shoppingapis.kelkoo.com' +
	'/V3/productSearch?query=ipod&sort=default_ranking&start=1&results=20&show_products=1&show_subcategories=1&show_refinements=1&' +
	'aid=96954747', 'c49KarBx')

	try:
		# request_string = str(
		# 	"http://se.shoppingapis.kelkoo.com/V3/productSearch?" +
		# 		"query=iPhone%20X%2064GB&" +
		# 		"sort=default_ranking&" +
		# 		"start=1&" + 
		# 		"results=20&" + 
		# 		"show_products=1&" +
		# 		"show_subcategories=1&" +
		# 		"show_refinements=1&" + 
		# 		"aid=96954747×tamp=1521995231&" + 
		# 		"hash=WPXecOP6qlfscHzBQewlOg--"
		# ).format()

		res = requests.get(req_url)
		
		print res.content

		dict_res = xmltodict.parse(res.content)
	except Exception as e:
		print("There was an error when fetching product data from Kelkoo: ", e)
	finally :
		print json.dumps(dict_res, indent=2)
		# return dict_res['findItemsAdvancedResponse']['searchResult']['item'][:4]

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
