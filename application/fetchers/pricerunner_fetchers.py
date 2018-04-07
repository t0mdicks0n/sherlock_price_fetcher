import requests
import json

def urlify(in_string) :
  return "%20".join(in_string.split())

# 'https://www.pricerunner.co.uk/public/search/suggest/uk?q=iPhone%20X' 
# https://www.pricerunner.co.uk/public/v0/pi-gs/1-4257585/uk?urlName=Mobile-Phones/Apple-iPhone-X-64GB-Compare-Prices
# 'https://www.pricerunner.dk/public/search/suggest/dk?q=iPhone%20X'
# 'https://www.pricerunner.dk/pl/1-4257585/Mobiltelefoner/Apple-iPhone-X-64GB-Sammenlign-Priser' -H 'pragma: no-cache' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,sv;q=0.8' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: no-cache' -H 'authority: www.pricerunner.dk' -H 'cookie: abtest=granular_view_type%7C1; pr_ga_traffic=Direct; mv=f; pr_sid=a93c5510839348d8826fff05b7478928; _ga=GA1.2.47613918.1523052807; _gid=GA1.2.1968747122.1523052807; cto_lwid=2e98eada-c209-4425-9da6-b4d9bc36032b; cookies_accept=true; _gat_UA-22423368-1=1; dmr=1; PHPSESSID=3al3377av9ssn6oebhejmbheu3; pr_trk=0%7C%7C%7C32%7C882a458464ee4f6aa67d906c76e19325%7Ctyped_link%7C%7C%7C%7C%7C%7C%7C%7C%7C%7C; _gat=1; pr_clickout=%5B%7B%22category%22%3A%22Mobiltelefoner(1)%22%7D%2C%7B%22hierarchy%22%3A%22Telefoni(4)%22%7D%2C%7B%22categoryType%22%3A%22Structured%22%7D%2C%7B%22trafficType%22%3A%22Direct%22%7D%2C%7B%22numberOfRetailers%22%3A%2247%22%7D%2C%7B%22numberOfLinks%22%3A%2233%22%7D%2C%7B%22numberOfReviews%22%3A%22100%2B%22%7D%2C%7B%22member%22%3A%22No%22%7D%2C%7B%22lastAction%22%3A%22undefined%22%7D%2C%7B%22searchKeyword%22%3A%22%22%7D%2C%7B%22searchType%22%3A%22%22%7D%2C%7B%22referralSite%22%3A%22%22%7D%2C%7B%22referralAd%22%3A%22%22%7D%2C%7B%22trafficTypeNew%22%3A%22Direct%22%7D%2C%7B%22ABTest%22%3A%22A%22%7D%2C%7B%22pageType%22%3A%22pl%22%7D%2C%7B%22firstAction%22%3A%22undefined%22%7D%2C%7B%22ABtestName%22%3A%22Klarna%20checkout%20for%20a%20merchant%22%7D%2C%7B%22dimension26%22%3A%2247%22%7D%2C%7B%22dimension27%22%3A%2233%22%7D%2C%7B%22dimension28%22%3A%220%22%7D%2C%7B%22dimension29%22%3A%22602%22%7D%2C%7B%22dimension30%22%3A%224.7%22%7D%2C%7B%22dimension31%22%3A%227532%20-%2010999%22%7D%2C%7B%22fallbackRule%22%3A%22%7B%7B__GA_FallbackRule__%7D%7D%22%7D%5D' --compressed

def get_country_link() :
	return {
		'UK': {
			'fetch_id': 'https://www.pricerunner.co.uk/public/search/suggest/uk?q=',
			'fetch_offers_1': 'https://www.pricerunner.co.uk/public/v0/pi-gs/',
			'fetch_offers_2': '/uk?urlName='
		},
		'SE': {
			'fetch_id': 'https://www.pricerunner.se/public/search/suggest/se?q=',
			'fetch_offers_1': 'https://www.pricerunner.se/public/v0/pl/',
			'fetch_offers_2': '/se?urlName='
		},
		'DK': {
			'fetch_id': 'https://www.pricerunner.dk/public/search/suggest/dk?q=',
			'fetch_offers_1': 'https://www.pricerunner.dk/public/v0/pl/',
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
	# url = 'https://www.pricerunner.se/public/v0/pl/' + product_url.split('/')[2] + '/se?urlName=' + '/'.join(product_url.split('/')[3:])
	url = get_country_link()[country]['fetch_offers_1'] + product_url.split('/')[2] + get_country_link()[country]['fetch_offers_2'] + '/'.join(product_url.split('/')[3:])
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
		print request.json()
		res = request.json()['product']['offers']
		return res
