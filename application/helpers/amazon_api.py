import json
import bottlenose
import xmltodict
import random
import time
from urllib2 import HTTPError

def error_handler(err):
	ex = err['exception']
	if isinstance(ex, HTTPError) and ex.code == 503:
		time.sleep(random.expovariate(0.1))
		return True

def get_amazon_object(region) :
	ama_keys = json.load(open('application/config/api_keys.json'))['amazon'][region]
	return bottlenose.Amazon(
		ama_keys['access_key'], ama_keys['secret_key'], ama_keys['associate_tag'],
		Region=region, ErrorHandler=error_handler, MaxQPS=0.9,
		Parser=lambda text: xmltodict.parse(text)
	)
