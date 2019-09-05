from fetchers import fetch_retailers_without_facebook
from fetchers import fetch_facebook_data
from dumpers import write_facebook_data

def iterate_and_scrape_facebook(retailers) :
	for retailer in retailers :
		print("Scraping Facebook Pages data on, " + retailer['retailer_url'])
		if retailer['retailer_url'][0] == 'w' :
			retailer_name = retailer['retailer_url'].split('.')[1]
		else :
			retailer_name = retailer['retailer_url'].split('.')[0]
		facebook_data = fetch_facebook_data(retailer_name)
		# Output the data to the database		
		write_facebook_data(
			retailer['id'],
			facebook_data['likes'],
			facebook_data['followers'],
			facebook_data['rating']
		)

def scrape_facebook() :
	retailers_without_facebook = fetch_retailers_without_facebook()
	iterate_and_scrape_facebook(retailers_without_facebook)