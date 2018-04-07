from jobs import sync_product_links as sync_pricerunner_products
from jobs import sync_pricerunner_offers
from jobs import sync_amazon_products
from jobs import sync_amazon_offers
from jobs import sync_ebay_offers
from jobs import sync_kelkoo_offers

import schedule
import time

def pricerunner() :
	sync_pricerunner_products('SE')
	sync_pricerunner_offers('SE')
	sync_pricerunner_products('DK')
	sync_pricerunner_offers('DK')
	# ----Fucked up result from the API 
	# sync_pricerunner_products('UK')
	# sync_pricerunner_offers('UK')

def amazon() :
	sync_amazon_products('UK')
	sync_amazon_offers('UK')
	sync_amazon_products('DE')
	sync_amazon_offers('DE')
	sync_amazon_products('IT')
	sync_amazon_offers('IT')
	sync_amazon_products('ES')
	sync_amazon_offers('ES')
	
def ebay () :
	sync_ebay_offers('UK')
	sync_ebay_offers('DE')
	sync_ebay_offers('FR')
	sync_ebay_offers('IT')
	# ----These does not work for some reason:
	# sync_ebay_offers('NL')
	# sync_ebay_offers('ES')

def kelkoo () :
	sync_kelkoo_offers('UK')
	sync_kelkoo_offers('DE')
	# sync_kelkoo_offers('SE')
	# sync_kelkoo_offers('FR')
	# sync_kelkoo_offers('NL')
	# sync_kelkoo_offers('DK')
	# sync_kelkoo_offers('FI')

if __name__ == '__main__' :
	print("Running the scheduler.")

	# schedule.every().day.at("00:00").do(ulog_pre_process)
	# schedule.every().day.at("03:00").do(invoice_data_write)

	schedule.every(2).minutes.do(kelkoo)

	while True:
		schedule.run_pending()
		time.sleep(1)
