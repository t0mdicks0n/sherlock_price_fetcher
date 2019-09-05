import requests
from bs4 import BeautifulSoup
import re

def grab_siterank(soup) :
	site_rank = None
	# Check that the metric exist, otherwise return none
	if len(soup.select(".rankmini-rank")) > 0 :
		# Regex out only integers
		site_rank = re.sub("[^0-9]", "", (soup.select(".rankmini-rank")[0]).text)
	return site_rank

def grab_daily_sec_on_site(soup) :
	daily_sec_on_site = None
	# Check that the metric exist, otherwise return none
	if len(soup.select(".rankmini-daily .rankmini-rank")) > 0 :
		# Grab and parse out the data as a string, 8:30 for example
		daily_min_as_string = ((soup.select(".rankmini-daily .rankmini-rank")[0]).text).strip()
		# Convert the string to minutes 8 * 60 + 30 in this instance
		daily_sec_on_site = (int(daily_min_as_string.split(':')[0]) * 60) + int(daily_min_as_string.split(':')[1])
	return daily_sec_on_site

def fetch_alexa_data(retailer_url) :
	try : 
		request_string = 'https://www.alexa.com/siteinfo/' + retailer_url
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
		}
		page = requests.get(request_string, timeout=5, headers=headers)
		if page.status_code != 200 :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when fetching data on an Alexa site: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		return {
			'site_rank': grab_siterank(soup),
			'daily_sec_on_site': grab_daily_sec_on_site(soup)
		}
