from database import Database

def fetch_products_without_pricerunner () :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				A.name
			FROM products A
			LEFT JOIN pricerunner B
			ON A.id = B.product_id
			WHERE B.product_id IS NULL;
		""")
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		return rows