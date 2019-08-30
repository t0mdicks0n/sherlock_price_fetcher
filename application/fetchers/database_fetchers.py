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
			SELECT * FROM (
				SELECT
					A.name,
					A.id,
					A.price::float / (SELECT to_sek FROM currency WHERE country = %s) AS price,
					row_number() OVER (PARTITION BY category ORDER BY popularity_idx ASC) AS rownum
				FROM products A
				LEFT JOIN (
					SELECT *
					FROM amazon
					WHERE amazon_country = %s
				) B
				ON A.id = B.product_id
				WHERE B.product_id IS NULL
				AND price > 0
			) prod_table
			-- Grab the 500 most popular products from each category
			WHERE rownum < 500
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
			--AND product_name LIKE 'Apple iPhone X%%'
			--LIMIT 100
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
			AND popularity_idx < 300
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

def fetch_products_without_prisjakt(country) :
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
				FROM prisjakt
				WHERE prisjakt_market = %s
			) B
			ON A.id = B.product_id
			WHERE B.product_id IS NULL
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		# Instead of data [{'name': 'MyPhone 1082', 'id': 1717}, {'name': 'MyPhone 1062 Talk+', 'id': 1718}]
		# I need {'MyPhone 1082': 1717, 'MyPhone 1062 Talk+': 1718}
		row_dict = {}
		for row in rows :
			row_dict[row['name']] = row['id']
		return row_dict

def fetch_prisjakt_products(country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				product_id,
				url
			FROM prisjakt
			WHERE URL IS NOT NULL
			AND prisjakt_market = %s
		""", (country,))
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_categories() :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				*
			FROM categories;
		""")
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows

def fetch_products_with_pj_images() :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				*
			FROM products
			WHERE image SIMILAR TO '%%pji%%|%%pricespy%%';
		""")
		rows = cur_dict.fetchall()
	except Exception as e :
		print("There was an error: ", e)
	finally :
		psql.close_connection()
		return rows