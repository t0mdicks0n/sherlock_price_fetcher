from database import Database

def get_live_offers_table() :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				CASE WHEN offers_1 IS TRUE THEN 'offers_1' ELSE 'offers_2' END AS live_offer_table
			FROM offers_table_rotation
		""")
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an erro getting the live offers table ", str(e))
	psql.close_connection()
	return rows

def write_offers(offers_data) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(offers_data) == 0 :
		return
	try :
		# Store the name of the live offers database in a variable
		live_offer_table = get_live_offers_table()[0]['live_offer_table']
		# Concatinate the input data to a long string for performance gains
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in offers_data)
		cur.execute("""
			INSERT INTO """ + live_offer_table + """ (
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
		""" + args_str + """
			ON CONFLICT (product_id, offer_source, retailer_name, retail_prod_name)
			DO UPDATE SET
				(price, shipping_cost, offer_url)
				= (EXCLUDED.price, EXCLUDED.shipping_cost, EXCLUDED.offer_url)
		""") 
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when writing offers data to DB: ", e)