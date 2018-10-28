from database import Database

def get_offers_table(extra_run=False) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		if extra_run : 
			cur_dict.execute("""
				SELECT
					-- I want to write all data to the offers table that is live when it's a extra run
					-- that is only updating the offers
					CASE WHEN offers_1 IS TRUE THEN 'offers_1' ELSE 'offers_2' END AS offer_table
				FROM offers_table_rotation
			""")
		else :
			cur_dict.execute("""
				SELECT
					-- I want to write all data to the offers table that isn't live
					CASE WHEN offers_1 IS TRUE THEN 'offers_2' ELSE 'offers_1' END AS offer_table
				FROM offers_table_rotation
			""")
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an erro getting the offers table for the purpose ", str(e))
	psql.close_connection()
	return rows

def write_offers(offers_data, extra_run=False, offer_table=None) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(offers_data) == 0 :
		return
	try :
		# Store the name of the live offers database in a variable
		if offer_table == None :
			offer_table = get_offers_table(extra_run)[0]['offer_table']
		# Concatinate the input data to a long string for performance gains
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s)", x) for x in offers_data)
		cur.execute("""
			INSERT INTO """ + offer_table + """ (
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