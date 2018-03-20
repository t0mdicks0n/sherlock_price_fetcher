import json
import requests
import xmltodict

def url_encode(string) :
	return "%20".join(string.split(" "))

def search_for_offer(api_key, country, product_name) :
	try:
		request_string = str("http://svcs.ebay.com/services/search/FindingService/v1?" + 
			"OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&" + 
			"SECURITY-APPNAME={0}&" + 
			"GLOBAL-ID=EBAY-GB&" +
			"RESPONSE-DATA-FORMAT=XML&" +
			"REST-PAYLOAD&" +
				"affiliate.networkId=9&" +
				"affiliate.trackingId=5338271690&" +
				"keywords={1}&" + 
				"itemFilter.name=Condition&itemFilter.value=New&" +
				"itemFilter.name=SellerBusinessType&itemFilter.value=Business"
		).format(
			api_key['APPNAME'],
			url_encode(product_name)
		)

		res = requests.get(request_string)
		dict_res = xmltodict.parse(res.content)

		print json.dumps(dict_res, indent=2)
	except Exception as e:
		print("There was an error when fetching product data from eBay: ", e)
