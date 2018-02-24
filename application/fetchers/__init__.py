from database import Database
import pprint

def testDB () :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur.execute("""
			SELECT *
			FROM products;
		""")
		rows = cur.fetchall()
		pprint.pprint(rows)
	except Exception as e :
		print("There was an error: ", e)
