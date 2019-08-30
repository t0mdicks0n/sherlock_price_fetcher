from database import Database

def write_products(products_data) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(products_data) == 0 :
		return
	try :
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", x) for x in products_data)
		cur.execute("""
			INSERT INTO products (
				name,
				category,
				image,
				price,
				popularity_idx
			) VALUES 
		""" + args_str + """
			ON CONFLICT (name, category)
			DO UPDATE SET
				(price, popularity_idx)
				= (EXCLUDED.price, EXCLUDED.popularity_idx)
		""") 
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when writing products to DB: ", e)

def update_image_url(new_img_url, product_id) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur.execute("""
			UPDATE products SET image = %s
			WHERE id = %s
		""", (new_img_url, product_id)) 
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when updating image url: ", e)