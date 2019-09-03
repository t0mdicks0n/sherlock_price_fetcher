import requests
from bs4 import BeautifulSoup
import re

def search_retailer(retailer_name) :
	try : 
		request_string = "https://www.trustpilot.com/search?query=" + "%20".join(retailer_name.split())
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		if page.status_code != 200 :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when searching for a retailer from Trustpilot: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		# We didn't find a match on the retailer name
		if len(soup.select(".no-search-results")) > 0 :
			return None
		# If there's only one search result Trustpilot displays that directly.
		# If that's the case, return the search URL for the next step
		elif len(soup.select(".badge-card__title")) > 0 :
			if (((soup.select(".badge-card__title")[0]).text).strip()) is not None :
				return request_string
		# If there are more then one result, return the URL to the top one
		elif len([a['href'] for a in soup.select(".search-result-heading")][0]) > 0 :
			return "https://www.trustpilot.com" + [a['href'] for a in soup.select(".search-result-heading")][0]
		# If there are no results, return None
		else :
			return None

def fetch_trustpilot_reviews(tp_site) :
	try : 
		request_string = tp_site
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		if page.status_code != 200 :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when fetching data on a Trustpilot site: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		# Declare a variable for the average rating
		first_alt = None
		# Iterate over all image tags with a class of star-rating
		for div in soup.find_all('div', 'star-rating'):
			for img in div.find_all('img', alt=True):
				# Grab the first image tags alt value and save into a variable
				if first_alt is None :
					# When they don't have any ratings we get something like "#rating/desc/star0#"
					if len(img['alt'].split(' ')[0]) > 1 :
						first_alt = 0
					else :
						first_alt = img['alt'].split(' ')[0]
		# Sometimes (with "rum21" for example) a Trustpilot profile exist but the store is closed
		num_ratings = None
		if len(soup.select(".headline__review-count")) > 0 :
			num_ratings = re.sub("[^0-9]", "", ((soup.select(".headline__review-count")[0]).text))
		# Return the above and the number of ratings which is easier to access
		return {
			'num_ratings': num_ratings,
			'avg_rating': first_alt,
			'retailer_url': ((soup.select(".badge-card__title")[0]).text).strip()
		}

def fetch_trustpilot_data(retailer_name) :
	tp_site_for_retailer = search_retailer(retailer_name)
	if tp_site_for_retailer is not None :
		return fetch_trustpilot_reviews(tp_site_for_retailer)
	else :
		print("Wasn't able to find a match at Trustpilot for retailer: ", retailer_name)
		return {
			'num_ratings': None,
			'avg_rating': None,
			'retailer_url': None
		}
