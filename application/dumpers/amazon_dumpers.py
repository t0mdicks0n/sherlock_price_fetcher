from database import Database

def write_amazon(amazon_data) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(amazon_data) == 0 :
		return
	try :
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", x) for x in amazon_data)
		cur.execute("""
			INSERT INTO amazon (
				product_id,
				amazon_country,
				asin_id,
				manufacturer,
				product_group,
				product_name,
				offer_url
			) VALUES
			""" + args_str)
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when writing amazon data to DB: ", e)
