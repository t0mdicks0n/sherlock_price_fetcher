from database import Database

def refresh_best_offers_matview() :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			REFRESH MATERIALIZED VIEW CONCURRENTLY best_offers_matview;
		""")
	except Exception as e :
		print("There was an error refreshing MV best_offers_matview: ", e)
	finally :
		connection.commit()
		psql.close_connection()