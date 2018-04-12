from database import Database

def write_products(products_data) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(products_data) == 0 :
		return
	try :
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s)", x) for x in products_data)
		cur.execute("""
			INSERT INTO products (
				name,
				category,
				image,
				price
			) VALUES 
		""" + args_str + """
			ON CONFLICT (name, category, image)
			DO UPDATE SET
				(price, image)
				= (EXCLUDED.price, EXCLUDED.image)
		""") 
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when writing products to DB: ", e)