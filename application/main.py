# coding: utf8
from jobs import sync_product_links as sync_pricerunner_products
from jobs import sync_pricerunner_offers
from jobs import sync_amazon_products
from jobs import sync_amazon_offers
from jobs import sync_ebay_offers
from jobs import sync_kelkoo_offers
from jobs import sync_kelkoo_offers
from jobs import offers_wipe
from jobs import sync_products
from jobs import sync_prisjakt_products
from jobs import sync_prisjakt_offers
from jobs import offers_support_wipe

import schedule
import time
import datetime

def pricerunner() :
	print(str(datetime.datetime.now()) + ": Starting Pricerunner.")
	sync_pricerunner_products('SE')
	sync_pricerunner_offers('SE')
	sync_pricerunner_products('DK')
	sync_pricerunner_offers('DK')
	# ----Fucked up result from the API 
	# sync_pricerunner_products('UK')
	# sync_pricerunner_offers('UK')
	print(str(datetime.datetime.now()) + ": Finished Pricerunner.")

def amazon() :
	print(str(datetime.datetime.now()) + ": Starting Amazon.")
	sync_amazon_products('UK')
	sync_amazon_offers('UK')
	sync_amazon_products('DE')
	sync_amazon_offers('DE')
	sync_amazon_products('IT')
	sync_amazon_offers('IT')
	sync_amazon_products('ES')
	sync_amazon_offers('ES')
	print(str(datetime.datetime.now()) + ": Finished Amazon.")

def amazon_only_offers() :
	print(str(datetime.datetime.now()) + ": Starting Amazon offers extra run.")
	sync_amazon_offers('UK', extra_run=True)
	sync_amazon_offers('DE', extra_run=True)
	sync_amazon_offers('IT', extra_run=True)
	sync_amazon_offers('ES', extra_run=True)
	print(str(datetime.datetime.now()) + ": Finished Amazon offers extra run.")

def ebay () :
	print(str(datetime.datetime.now()) + ": Starting eBay.")
	sync_ebay_offers('UK')
	sync_ebay_offers('DE')
	sync_ebay_offers('FR')
	sync_ebay_offers('IT')
	# ----These does not work for some reason:
	# sync_ebay_offers('NL')
	# sync_ebay_offers('ES')
	print(str(datetime.datetime.now()) + ": Finished eBay.")

def kelkoo () :
	print(str(datetime.datetime.now()) + ": Starting Kelkoo.")
	sync_kelkoo_offers('UK')
	sync_kelkoo_offers('DE')
	sync_kelkoo_offers('SE')
	sync_kelkoo_offers('FR')
	sync_kelkoo_offers('NL')
	sync_kelkoo_offers('DK')
	sync_kelkoo_offers('FI')
	print(str(datetime.datetime.now()) + ": Finished Kelkoo.")

def prisjakt () :
	print(str(datetime.datetime.now()) + ": Starting Prisjakt.")
	sync_products("smartphones")
	sync_prisjakt_products('SE')
	sync_prisjakt_offers('SE')
	print(str(datetime.datetime.now()) + ": Finished Prisjakt.")

def deleting_support_tables() :
	print(str(datetime.datetime.now()) + ": Deleting supporting tables.")
	offers_support_wipe()
	print(str(datetime.datetime.now()) + ": Finished deleting supporting tables.")

def rotate_offers_table () :
	print(str(datetime.datetime.now()) + ": Deleting offers data.")
	offers_wipe()
	print(str(datetime.datetime.now()) + ": Finished deleting offers data.")

if __name__ == '__main__' :
	print(str(datetime.datetime.now()) + ": Sherlock launched successfully.")
	print(str(datetime.datetime.now()) + ": Now running the scheduler.")

	# schedule.every().hour.do(job, param1, param2)

	# sync_amazon_offers('UK')
	# schedule.every(1).minutes.do(amazon)

	# Nightly run
	schedule.every().day.at("01:00").do(deleting_support_tables)
	schedule.every().day.at("01:00").do(amazon)
	schedule.every().day.at("01:00").do(pricerunner)
	schedule.every().day.at("01:00").do(ebay)
	schedule.every().day.at("01:00").do(kelkoo)
	schedule.every().day.at("01:00").do(prisjakt)
	schedule.every().day.at("01:00").do(rotate_offers_table)

	# Daily run
	schedule.every().day.at("13:00").do(deleting_support_tables)
	schedule.every().day.at("13:00").do(amazon)
	schedule.every().day.at("13:00").do(pricerunner)
	schedule.every().day.at("13:00").do(ebay)
	schedule.every().day.at("13:00").do(kelkoo)
	schedule.every().day.at("13:00").do(prisjakt)
	schedule.every().day.at("13:00").do(rotate_offers_table)

	# Extra Amazon offers run
	schedule.every().day.at("11:00").do(amazon_only_offers)
	schedule.every().day.at("17:00").do(amazon_only_offers)

	# amazon_only_offers()

	while True:
		schedule.run_pending()
		time.sleep(1)
