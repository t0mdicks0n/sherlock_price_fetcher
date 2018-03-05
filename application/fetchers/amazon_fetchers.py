
def format_price(price) :
	return format(price, '.2f').replace('.', '')

def search_for_product(product_name, amazon, price) :
	try : 
		response = amazon.ItemSearch(
			Keywords=product_name,
			SearchIndex="All",
			Condition="New",
			# Provide a minimum price for better results
			MinimumPrice=format_price(price * 0.5)
		)
	except Exception as e:
		print "There was an error when calling the Amazon API: ", e
	finally :
		return response['ItemSearchResponse']['Items']['Item'][0]

def search_for_offer(asin, amazon) :
	try :
		response = amazon.ItemLookup(
			ItemId=asin,
			ResponseGroup="Offers",
			IdType="ASIN",
			Condition="New"
		)
	except Exception as e:
		print "There was an error when calling the Amazon API: ", e
	finally :
		return response['ItemLookupResponse']['Items']['Item']['Offers']['Offer']
