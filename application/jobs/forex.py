import json

from fetchers import get_latest_forex
from fetchers import get_latest_exchange_rate
from dumpers import write_currency

def calc_forex_pairs_in_sek(euro_to_sek, euro_to_wanted_currency) :
	return euro_to_sek / euro_to_wanted_currency

def get_and_update_forex() :
	api_key = json.load(open('application/config/api_keys.json'))['fixerio']
	data = get_latest_forex(api_key)
	# Calculate the forex pairs and write them to the database
	write_currency(
		exchange_rate=data['rates']['SEK'],
		countries=['DE', 'IT', 'ES', 'FR', 'NL', 'FI'],
		to_sek=True
	)
	write_currency(
		exchange_rate=calc_forex_pairs_in_sek(data['rates']['SEK'], data['rates']['GBP']),
		countries=['UK'],
		to_sek=True
	)
	write_currency(
		exchange_rate=calc_forex_pairs_in_sek(data['rates']['EUR'], data['rates']['GBP']),
		countries=['UK'],
		to_sek=False
	)
	write_currency(
		exchange_rate=calc_forex_pairs_in_sek(data['rates']['SEK'], data['rates']['DKK']),
		countries=['DK'],
		to_sek=True
	)
	write_currency(
		exchange_rate=calc_forex_pairs_in_sek(data['rates']['EUR'], data['rates']['DKK']),
		countries=['DK'],
		to_sek=False
	)