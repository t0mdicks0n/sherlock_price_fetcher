from google.cloud import storage
import requests

def persist_image(image_url, product_id) :
	# Initiate a client
	storage_client = storage.Client.from_service_account_json(
		'application/config/cloud_storage_key.json'
	)
	# Choose bucket
	bucket = storage_client.get_bucket('panprices')
	# Define name of the file you want to upload
	blob = bucket.blob(
		'products/' + str(product_id) + '.jpg'
	)
	try :
		request = requests.get(image_url)
	except requests.exceptions.RequestException as e :
		print("There was an error fetching the image URL: ", e)
	finally :
		# Upload the image as a string to this blob defined earlier
		blob.upload_from_string(
			request.content,
			content_type='image/jpg'
		)
		# Return the URL of the newly created image
		return 'https://storage.cloud.google.com/panprices/products/' + str(product_id) + '.jpg'