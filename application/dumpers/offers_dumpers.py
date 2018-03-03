from database import Database

def write_offers(offers_data) :
	# print offers_data
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(offers_data) == 0 :
		return
	try :
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in offers_data)
		cur.execute("""
			INSERT INTO offers (
				product_id,
				offer_source,
				retail_prod_name,
				retailer_name,
				country,
				price,
				shipping_cost,
				int_shipping,
				offer_url
			) VALUES 
		""" + args_str) 
		connection.commit()
	except Exception as e :
		print("There was an error when writing offers data to DB: ", e)

	# product_id INTEGER,
	# offer_source TEXT,
	# retail_prod_name TEXT,
	# retailer_name TEXT,
	# country TEXT,
	# price INTEGER,
	# shipping_cost INTEGER,
	# int_shipping BOOLEAN,
	# offer_url TEXT