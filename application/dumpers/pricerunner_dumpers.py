from database import Database
from helpers import IteratorFile
import pprint

def write_pricerunner (product_data) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(product_data) == 0 :
		return
	try :
		args_str = ','.join(cur.mogrify("(%s, %s, %s, %s)", x) for x in product_data)
		cur.execute("""
			INSERT INTO pricerunner (
				country,
				product_id,
				url,
				lowest_price
			) VALUES 
		""" + args_str) 
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when writing pricerunner data to DB: ", e)