from database import Database

def fetch_products_without_pricerunner (country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				A.name,
				A.id
			FROM products A
			LEFT JOIN (
				SELECT *
				FROM pricerunner
				WHERE country = %s
			) B
			ON A.id = B.product_id
			WHERE B.product_id IS NULL
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_pricerunner_products (country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				product_id,
				url
			FROM pricerunner
			WHERE URL IS NOT NULL
			AND country = %s
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_products_without_amazon (country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				A.name,
				A.id,
				A.price::float / (SELECT to_sek FROM currency WHERE country = %s) AS price
			FROM products A
			LEFT JOIN (
				SELECT *
				FROM amazon
				WHERE amazon_country = %s
			) B
			ON A.id = B.product_id
			WHERE B.product_id IS NULL
			AND price > 0
		""", (country, country))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_amazon_products (country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				product_id,
				amazon_country,
				asin_id,
				product_name,
				offer_url
			FROM amazon
			WHERE asin_id IS NOT NULL
			AND amazon_country = %s
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_products_without_ebay (country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				name,
				id,
				price::float / (SELECT to_sek FROM currency WHERE country = %s) AS price
			FROM products
			WHERE price > 0
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_products_without_kelkoo(country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				name,
				id,
				price::float / (SELECT to_sek FROM currency WHERE country = %s) AS price
			FROM products
			WHERE price > 0
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows	

