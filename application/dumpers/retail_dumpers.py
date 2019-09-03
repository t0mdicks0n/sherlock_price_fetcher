from database import Database

def write_trustpilot_rating(retailer_id, avg_rating, num_ratings, retailer_url) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur.execute("""
			INSERT INTO trustpilot (
				retailer_id,
				avg_rating,
				num_ratings,
				retailer_url
			) VALUES (
				%s,
				%s,
				%s,
				%s
			)
			ON CONFLICT (retailer_id)
			DO UPDATE SET (
				retailer_id,
				avg_rating,
				num_ratings,
				retailer_url
			) = (
				EXCLUDED.retailer_id,
				EXCLUDED.avg_rating,
				EXCLUDED.num_ratings,
				EXCLUDED.retailer_url
			)
		""", (retailer_id, avg_rating, num_ratings, retailer_url))
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error writing trustpilot data: ", e)

def write_alexa_rating(retailer_id, site_rank) :
	psql = Database()
	cur, cur_dict, connection, psycopg2 = psql.get_connection()
	try :
		cur.execute("""
			INSERT INTO alexa (
				retailer_id,
				site_rank
			) VALUES (
				%s,
				%s
			)
			ON CONFLICT (retailer_id)
			DO UPDATE SET (
				retailer_id,
				site_rank
			) = (
				EXCLUDED.retailer_id,
				EXCLUDED.site_rank
			)
		""", (retailer_id, site_rank))
		connection.commit()
		psql.close_connection()
	except Exception as e :
		print("There was an error writing alexa data: ", e)
