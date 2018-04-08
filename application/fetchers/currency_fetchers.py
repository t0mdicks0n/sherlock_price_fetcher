from database import Database

def fetch_exchange_rate(country) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			SELECT
				to_sek AS rate
			FROM currency
			WHERE country = %s
		""", (country,))
	except Exception as e :
		print("There was an error fetching exchange rates: ", e)
	finally :
		rows = cur_dict.fetchall()
		psql.close_connection()
		return rows[0]
