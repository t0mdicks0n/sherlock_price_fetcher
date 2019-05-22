import json
import requests
import xmltodict

def url_encode(string) :
	return "%20".join(string.split(" "))

def search_for_offer(api_key, country, product_name, price) :
	if country is 'UK' :
		country = 'GB'
	try:
		request_string = str("http://svcs.ebay.com/services/search/FindingService/v1?" + 
			"OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&" + 
			"SECURITY-APPNAME={0}&" + 
			"GLOBAL-ID=EBAY-{1}&" +
			"RESPONSE-DATA-FORMAT=XML&" +
			"REST-PAYLOAD&" +
				"affiliate.networkId=9&" +
				"affiliate.trackingId=5338271690&" +
				"keywords={2}&" + 
				"itemFilter(0).name=Condition&itemFilter(0).value=1000&" +
				"itemFilter(1).name=SellerBusinessType&itemFilter(1).value=Business&" +
				"itemFilter(2).name=TopRatedSellerOnly&itemFilter(2).value=true&" +
				"itemFilter(3).name=HideDuplicateItems&itemFilter(3).value=true&" +
				"itemFilter(4).name=MinPrice&itemFilter(4).value={3}&" +
				"outputSelector=SellerInfo"
		).format(
			api_key['APPNAME'],
			country,
			url_encode(product_name),
			str(float(price) * 0.75)
		)
		res = requests.get(request_string)
		dict_res = xmltodict.parse(res.content)
	except Exception as e:
		print("There was an error when fetching product data from eBay: ", e)
	finally :
		# print json.dumps(dict_res['findItemsAdvancedResponse']['searchResult']['item'][:4], indent=2)
		# print json.dumps(dict_res, indent=2)
		return dict_res['findItemsAdvancedResponse']['searchResult']['item'][:4]
