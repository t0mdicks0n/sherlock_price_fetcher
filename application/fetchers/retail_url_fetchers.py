import requests

def get_merchant_id_from_kelkoo_offer(offer_url) :
	# It can look like this: https://de-go.kelkoogroup.net/ctl/go/sitesearchGo?.ts=1569789638691&.sig=FDOCMRJDQ06BBaDC9ZjzpXBe.Wo-&affiliationId=96954745&catId=138001&comId=11535213&contextLevel=1&contextOfferPosition=1&contextPageSize=19&country=de&ecs=ok&merchantid=11535213&offerId=c49cd3131f6ee89d5f80bbc3da155fc8&searchId=10769920718571_1569789638598_263661&searchQuery=Z3JhZG8gaWdl&service=5&wait=true
	return offer_url.split('&merchantid=')[1].split('&')[0]

def format_kelkoo(offer_source, kelkoo_keys, offer_url) :
	country = offer_source[-2:]
	return str(
		'https://europe-west1-panprices.cloudfunctions.net/kelkoo_merchant?offer_url=' +
		offer_url + '&api_key_id=' + kelkoo_keys.get(country)['id'] + '&api_key=' + kelkoo_keys.get(country)['key'] +
		'&merchant_id=' + get_merchant_id_from_kelkoo_offer(offer_url) + '&country=' + country
	)

def get_endpoint(offer_source, kelkoo_keys, offer_url) :
	if offer_source[0:6] == 'kelkoo' :
		print format_kelkoo(offer_source, kelkoo_keys, offer_url)
		return format_kelkoo(offer_source, kelkoo_keys, offer_url)
	elif offer_source[0:8] == 'prisjakt' :
		return 'https://europe-west1-panprices.cloudfunctions.net/prisjakt_merchant?offer_url=' + offer_url
	else :
		return 'https://europe-west1-panprices.cloudfunctions.net/pricerunner_merchant?offer_url=' + offer_url

def fetch_url_from_offer(offer_url, offer_source, kelkoo_keys) :
	offer_source_endpoint = get_endpoint(offer_source, kelkoo_keys, offer_url)
	try :
		request_string = offer_source_endpoint
		headers = {
			'User-Agent': "Sherlock"
		}

		print request_string
		response = requests.get(
			request_string,
			timeout=10,
			headers=headers
		)
	except Exception as e :
		print("There was an error when fetching data on a Facebook page: ", e)
	finally :
		return response.json()
