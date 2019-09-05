import requests
from bs4 import BeautifulSoup
import re

def format_fb_str_to_int(string) :
	# FB presents 739K instead of 739000 fix this
	adjusted_for_k = string.replace('K', '000')
	adjusted_for_m = adjusted_for_k.replace('M', '000000')
	remove_non_integer_chars = re.sub("[^0-9]", "", adjusted_for_m)
	return int(remove_non_integer_chars)

def try_pattern(soup, wanted_pattern, split_on) :
	'''
		Notes on this: Facebook's CSS is really really strange. The CSS classes
		in combination with IDs are never consistent for some strange reason.
		What I did find consistency in was the class and a pattern that always
		seems to emerge before the actual number of likes. This in combination
		with a data tag called "nt" generates some consistency. This function is
		iterating over all data rows with the matching class and looks for this
		specific pattern. Then when it finds it, it returns.
	'''
	patterns_matched = 0
	for nt in soup.find_all('div', {"class": ["_59k", "_2rgt", "_1j-f", "_2rgt"]}) :
		row = nt.get_text().split('Total likes3')[0]
		# Base case, if we have found the three patterns in a row return
		if patterns_matched == len(wanted_pattern) :
			# Grab the data then format it
			wanted_raw_data = row.split(split_on)[0]
			if wanted_raw_data == '' :
				return None
			else :
				return format_fb_str_to_int(wanted_raw_data)
		# Otherwise, test the pattern
		if row == wanted_pattern[patterns_matched] :
			patterns_matched = patterns_matched + 1
		# Start over if one of the rows dosen't adhere to the pattern
		else :
			patterns_matched = 0

def grab_likes(soup) :
	# This pattern always appear before the number of likes data
	pattern_1_match = try_pattern(soup, ['', 'Liked', ''], 'Total likes')
	# pattern_2_match = try_pattern(soup, ['Website', 'Website', ''], 'Total likes')
	if pattern_1_match == None :
		return try_pattern(soup, ['Website', 'Website', ''], 'Total likes')
	else :
		return pattern_1_match

def grab_followers(soup) :
	# This pattern always appear before the number of likes data
	wanted_pattern = ['Total likes', '']
	# This pattern always appear before the number of likes data
	pattern_1_match = try_pattern(soup, ['Total likes', ''], 'Total follows')
	return pattern_1_match

def grab_rating(soup) :
	# TODO: Implement this at some point
	return None

def fetch_facebook_data(retailer_name) :
	try : 
		request_string = "https://m.facebook.com/" + retailer_name + "/community"
		headers = {
			'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
		}
		page = requests.get(request_string, timeout=15, headers=headers)
		nothing_found = False
		if page.status_code == 404 :
			print "Nothing was found at URL: ", request_string
			nothing_found = True
		if (page.status_code != 200) and (page.status_code != 404) :
			print 'Got a bad status Code: ', page.status_code
	except Exception as e:
		print("There was an error when fetching data on a Facebook page: ", e)
	finally :
		soup = BeautifulSoup(page.content, 'html.parser')
		if nothing_found is True :
			return {
				'likes': None,
				'followers': None,
				'rating': None
			}
		else :
			return {
				'likes': grab_likes(soup),
				'followers': grab_followers(soup),
				'rating': grab_rating(soup)
			}