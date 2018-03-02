from database import Database
from helpers import IteratorFile
import pprint

def write_pricerunner (product_data) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	if len(product_data) == 0 :
		return
	try :
		# formated = IteratorFile(("{}\t{}\t{}".format(i[0], i[1], i[2]) for i in product_data))
		# cur.copy_from(formated, 'pricerunner', columns=('product_id', 'url', 'lowest_price'))
		args_str = ','.join(cur.mogrify("(%s,%s,%s)", x) for x in product_data)
		cur.execute("""
			INSERT INTO pricerunner (
				product_id,
				url,
				lowest_price
			) VALUES 
		""" + args_str) 
		connection.commit()
	except Exception as e :
		print("There was an error when writing pricerunner data to DB: ", e)