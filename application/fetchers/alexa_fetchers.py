import requests
from bs4 import BeautifulSoup
import re

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
		site_rank = None
		if len(soup.select(".rankmini-rank")) > 0 :
			site_rank = re.sub("[^0-9]", "", (soup.select(".rankmini-rank")[0]).text)
		# Return the result in right format
		return {
			'site_rank': site_rank
		}