from database import Database

def delete_offer_support_tables () :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			DELETE FROM pricerunner;
			DELETE FROM prisjakt;
			-- Amazon currently takes a lot of time to fetch products for
			DELETE FROM amazon;
		""")
	except Exception as e :
		print("There was an error wiping out supporting tables for the offers: ", e)
	finally :
		connection.commit()
		psql.close_connection()

def delete_offers() :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur_dict.execute("""
			UPDATE offers_table_rotation
			SET offers_1 = CASE WHEN offers_1 IS TRUE THEN FALSE ELSE TRUE END,
					offers_2 = CASE WHEN offers_2 IS TRUE THEN FALSE ELSE TRUE END,
					updated_at = now()
			WHERE id = 1;
			-- Delete all offers from the table that is not longer live
			SELECT delete_offers();
		""")
	except Exception as e :
		print("There was an error wiping out old offer data and rotating the tables: ", e)
	finally :
		connection.commit()
		psql.close_connection()

