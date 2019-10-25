from fetchers import fetch_retailers_without_domain
from fetchers import fetch_url_from_offer
import json

def iterate_and_fetch_domains(offers) :
	kelkoo_keys = json.load(open('application/config/api_keys.json'))['kelkoo_ecommerce_service']
	for offer in offers :
		print(offer)
		url_data = fetch_url_from_offer(offer['offer_url'], offer['offer_source'], kelkoo_keys)
		print url_data.get('logo')
		print {
			"offer_url": offer['offer_url'],
			"retailer_name": offer['retailer_name'],
			"offer_source": offer['offer_source'],
			"domain": url_data['domain'],
			"redirect_url": url_data.get('redirect_url'),
			"delivery_countries": url_data.get('delivery_countries'),
			"delivery_countries": url_data.get('delivery_countries'),
			"logo": url_data.get('logo')
		}

def fetch_domains_from_offers() :
	retailers_without_domain = fetch_retailers_without_domain()
	iterate_and_fetch_domains(retailers_without_domain)