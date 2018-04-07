import psycopg2
import psycopg2.extras
import json
import sys
import os

class Database :
	def __init__(self) :
		if 'POSTGRES_CONNECTION' in os.environ :
			try :
				connection = psycopg2.connect(
					dbname = os.environ['POSTGRES_DBNAME'],
					user = os.environ['POSTGRES_USER'],
					password = os.environ['POSTGRES_PASSWORD'],
					sslmode = "disable",
					application_name='Sherlock',
					host='127.0.0.1'
				)
			except psycopg2.OperationalError as e:
				print('Unable to connect to the Panprices Database!\n{0}').format(e)
			finally :
				cur = connection.cursor()
				cur_dict = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		elif 'DOCKER' in os.environ :
			try :
				connection = psycopg2.connect(
					dbname = "postgres",
					user = "postgres",
					hostaddr = "104.155.10.83",
					host = "kivra-bi:invoicedb",
					password = "PopA5m0aLF1D4x57",
					sslmode = "verify-full",
					sslrootcert = "/usr/src/app/certs/gcp_invoice/gce_ca.pem",
					sslcert = "/usr/src/app/certs/gcp_invoice/gce_cert.pem",
					sslkey = "/usr/src/app/certs/gcp_invoice/gce_key.pem",
					application_name='Ulog BI Data Dumper'
				)
			except psycopg2.OperationalError as e:
				print('Unable to connect to the GCE Invoice DB!\n{0}').format(e)
			finally :
				cur = connection.cursor()
				cur_dict = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		else :
			try :
				connection = psycopg2.connect(
					dbname = "prices_prod",
					user = "postgres",
					hostaddr = "35.195.14.142",
					host = "panprices:panprices-psql",
					password = "9GAfs882PI1t9MDG",
					sslmode = "verify-full",
					sslrootcert = "/Users/Tom/cert/panprices/server-ca.pem",
					sslcert = "/Users/Tom/cert/panprices/client-cert.pem",
					sslkey = "/Users/Tom/cert/panprices/client-key.pem",
					application_name='Sherlock Price Fetcher'
				)
			except psycopg2.OperationalError as e:
				print('Unable to connect to the Panprices Database!\n{0}').format(e)
			finally :
				cur = connection.cursor()
				cur_dict = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

		self.cur = cur
		self.cur_dict = cur_dict
		self.connection = connection
		self.psycopg2 = psycopg2

	def get_connection(self) :
		return [self.cur, self.cur_dict, self.connection, self.psycopg2]

	def close_connection(self) :
		self.cur.close()
		self.cur_dict.close()
		self.connection.close()
