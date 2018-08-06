from helpers import delete_offers
from helpers import delete_offer_support_tables

def offers_wipe() :
	delete_offers()

def offers_support_wipe() :
	delete_offer_support_tables()
