from pricerunner_fetchers import fetch_product_id

from database import Database
import pprint

def fetch_products () :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT *
			FROM products;
		""")
		rows = cur_dict.fetchall()
		pprint.pprint(rows)
	except Exception as e :
		print("There was an error: ", e)
