from database import Database

def delete_offers() :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			DELETE FROM pricerunner;
			DELETE FROM prisjakt;
			-- Amazon currently takes to much time to fetch products for
			-- DELETE FROM amazon;
			DELETE FROM offers;
		""")
	except Exception as e :
		print("There was an error wiping out old offer data and their supporting tables: ", e)
	finally :
		connection.commit()
		psql.close_connection()
