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
from jobs import get_and_update_forex
from jobs import sync_best_int_offers

import schedule
import time
import datetime
import argparse

def pricerunner() :
	print(str(datetime.datetime.now()) + ": Starting Pricerunner.")
	sync_pricerunner_products('SE')
	sync_pricerunner_offers('SE')
	sync_pricerunner_products('DK')
	sync_pricerunner_offers('DK')
	sync_pricerunner_products('UK')
	sync_pricerunner_offers('UK')
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

def kelkoo() :
	print(str(datetime.datetime.now()) + ": Starting Kelkoo.")
	sync_kelkoo_offers('UK')
	sync_kelkoo_offers('DE')
	sync_kelkoo_offers('SE')
	sync_kelkoo_offers('FR')
	sync_kelkoo_offers('NL')
	sync_kelkoo_offers('DK')
	sync_kelkoo_offers('FI')
	print(str(datetime.datetime.now()) + ": Finished Kelkoo.")

def prisjakt() :
	print(str(datetime.datetime.now()) + ": Starting Prisjakt.")
	# sync_products()
	print(str(datetime.datetime.now()) + ": Finished scraping products from Prisjakt.")
	sync_prisjakt_products('SE')
	sync_prisjakt_offers('SE')
	print(str(datetime.datetime.now()) + ": Finished Prisjakt.")

def prisjakt_products() :
	print(str(datetime.datetime.now()) + ": Starting Prisjakt Products.")
	sync_products()
	print(str(datetime.datetime.now()) + ": Finished Prisjakt Products.")	

def deleting_support_tables() :
	print(str(datetime.datetime.now()) + ": Deleting supporting tables.")
	offers_support_wipe()
	print(str(datetime.datetime.now()) + ": Finished deleting supporting tables.")

def rotate_offers_table() :
	print(str(datetime.datetime.now()) + ": Deleting offers data.")
	offers_wipe()
	print(str(datetime.datetime.now()) + ": Finished deleting offers data.")

def forex() :
	print(str(datetime.datetime.now()) + ": Fetching and updating forex exchange rates.")
	get_and_update_forex()
	print(str(datetime.datetime.now()) + ": Finished updating forex exchange rates.")

def best_international_offers() :
	print(str(datetime.datetime.now()) + ": Starting the international best offers database job.")
	sync_best_int_offers()
	print(str(datetime.datetime.now()) + ": Finished the international best offers database job.")

if __name__ == '__main__' :
	# Instantiate the parser
	parser = argparse.ArgumentParser(
		description='Kivra Invoicing Calculator',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
   _____ _               _            _    
  / ____| |             | |          | |   
 | (___ | |__   ___ _ __| | ___   ___| | __
  \___ \| '_ \ / _ \ '__| |/ _ \ / __| |/ /
  ____) | | | |  __/ |  | | (_) | (__|   < 
 |_____/|_| |_|\___|_|  |_|\___/ \___|_|\_\
                                           
                                                                                         
	""")
	# Define the arguments
	parser.add_argument(
		'-a',
		'--amazon',
		action='store_true',
		help='Calculates Amazon.'
	)
	parser.add_argument(
		'-pr',
		'--pricerunner',
		action='store_true',
		help='Calculates Pricerunner.'
	)
	parser.add_argument(
		'-e',
		'--ebay',
		action='store_true',
		help='Calculates eBay.'
	)
	parser.add_argument(
		'-k',
		'--kelkoo',
		action='store_true',
		help='Calculates Kelkoo.'
	)
	parser.add_argument(
		'-pj',
		'--prisjakt',
		action='store_true',
		help='Calculates Prisjakt.'
	)
	parser.add_argument(
		'-pjpr',
		'--prisjakt_products',
		action='store_true',
		help='Calculates Prisjakt.'
	)
	parser.add_argument(
		'-d',
		'--deleting-support-tables',
		action='store_true',
		help='Delete all support tables.'
	)
	parser.add_argument(
		'-r',
		'--rotate-offers-table',
		action='store_true',
		help='Rotates the offers tables.'
	)
	parser.add_argument(
		'-ao',
		'--amazon-only-offers',
		action='store_true',
		help='Only fetch prices for existing offers for Amazon.'
	)
	parser.add_argument(
		'-fx',
		'--forex',
		action='store_true',
		help='Fetch current forex exchange rates and write to DB.'
	)
	parser.add_argument(
		'-bo',
		'--best-offers',
		action='store_true',
		help='Run the international best offers database job.'
	)
	# Print the help
	# parser.print_help()
	# Parse the arguments
	args = parser.parse_args()

	if args.amazon :
		amazon()
	elif args.amazon_only_offers :
		amazon_only_offers()
	elif args.deleting_support_tables :
		deleting_support_tables()
	elif args.ebay :
		ebay()
	elif args.kelkoo :
		kelkoo()
	elif args.pricerunner :
		pricerunner()
	elif args.prisjakt :
		prisjakt()
	elif args.prisjakt_products :
		prisjakt_products()
	elif args.rotate_offers_table :
		rotate_offers_table()
	elif args.forex :
		forex()
	elif args.best_offers :
		best_international_offers()
	else :
		print str(datetime.datetime.now()) + "No option provided for Sherlock to execute."