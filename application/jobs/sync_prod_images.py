from fetchers import fetch_products_with_pj_images
from helpers import persist_image
from dumpers import update_image_url
from helpers import threaded_execution

def iterate_and_persist_images(products, country=None) :
	# TODO: The threaded execution expects a country variable and is
	# thus not general. Fix this.
	for product in products :
		# Persist the image and generate the new URL on Cloud Storage
		pp_img_url = persist_image(
			product['image'],
			product['id']
		)
		# Update the specific product with it's new URL
		update_image_url(pp_img_url, product['id'])
		print "Updated image URL for product " + str(product['id'])

def persist_pj_prod_images() :
	product_img_to_persist = fetch_products_with_pj_images()
	# Multi thread the execution
	threaded_execution(
		product_img_to_persist,
		iterate_and_persist_images,
		user_define_job=True
	)
