from fetchers import fetch_exchange_rate

def amazon_value_to_sek(value, exchange_rate) :
	return int(float(value[:-2] + '.' + value[-2:]) * exchange_rate['rate'])
