import json
import requests

def get_latest_forex(api_key) :
	try:
		res = requests.get(
			'http://data.fixer.io/api/latest?access_key=' + api_key
		)
	except Exception as e:
		print("There was an error when fetching forex exchange rates from fixerio: ", e)
	finally :
		json_dict = json.loads(res.content)
		# print json.dumps(json_dict, indent=2)
		return json_dict

def get_latest_exchange_rate(api_key, currency_from, currency_to, amount=1) :
	# CURRENTLY NOT SUPPORTED BY THE FREE VERSION OF THE API
	try:
		request_string = str(
			'http://data.fixer.io/api/latest?' + 
			'access_key={0}&' +
			'from={1}&' +
			'to={2}&' +
			'amount={3}'
		).format(
			api_key,
			currency_from,
			currency_to,
			amount
		)
		res = requests.get(request_string)
	except Exception as e:
		print("There was an error when converting a exchange rate from fixerio: ", e)
	finally :
		json_dict = json.loads(res.content)
		# print json.dumps(json_dict, indent=2)
		return json_dict