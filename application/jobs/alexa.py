from fetchers import fetch_retailers_without_alexa
from fetchers import fetch_alexa_data
from dumpers import write_alexa_rating

def iterate_and_scrape_alexa(retailers) :
	for retailer in retailers :
		print("Scraping Alexa for data on ", retailer['retailer_url'])
		alexa_data = fetch_alexa_data(retailer['retailer_url'])
		write_alexa_rating(
			retailer['id'],
			alexa_data['site_rank']
		)

def scrape_alexa() :
	retailers_without_alexa = fetch_retailers_without_alexa()
	iterate_and_scrape_alexa(retailers_without_alexa)