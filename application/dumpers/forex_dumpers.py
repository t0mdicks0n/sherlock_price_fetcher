from database import Database

def write_currency(exchange_rate, countries, to_sek=True) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		if to_sek :
			cur.execute("""
				UPDATE currency
				SET to_sek = %s
				WHERE country IN %s;
			""", [exchange_rate, tuple(countries)])
		else :
			cur.execute("""
				UPDATE currency
				SET to_eur = %s
				WHERE country IN %s;
			""", [exchange_rate, tuple(countries)])
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error when writing exchange rate to DB: ", e)
