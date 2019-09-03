from fetchers import fetch_retailers_without_trustpilot
from fetchers import fetch_trustpilot_data
from dumpers import write_trustpilot_rating

def interate_and_scrape_trustpilot(retailers) :
	for retailer in retailers :
		print("Scraping Trustpilot for data on ", retailer['name'])
		tp_data = fetch_trustpilot_data(retailer['name'])
		# Write the data we scraped to the database if we found a
		# Trustpilot match
		write_trustpilot_rating(
			retailer['id'],
			tp_data['avg_rating'],
			tp_data['num_ratings'],
			tp_data['retailer_url']
		)

def scrape_trustpilot() :
	retailers_without_trustpilot = fetch_retailers_without_trustpilot()
	interate_and_scrape_trustpilot(retailers_without_trustpilot)
