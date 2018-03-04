

def search_for_offer (product_name, amazon) :
	response = amazon.ItemSearch(Keywords=product_name, SearchIndex="All", ResponseGroup="Offers")
	return response
