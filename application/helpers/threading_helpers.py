import threading

def split_tuple(input_data, wanted_num=30) :
	num_in_each_bucket = (len(input_data) + 1) / wanted_num
	buckets = []
	bucket = []
	for data_row in input_data :
		if len(bucket) > num_in_each_bucket :
			buckets.append(bucket)
			bucket = []
		bucket.append(data_row)
	buckets.append(bucket)
	# Free memory just in case
	del input_data
	return buckets

def iterate_over_bucket(bucket, func_to_execute) :
	for row in enumerate(bucket) :
		func_to_execute(row)
	# Free memory just in case
	del bucket

def threaded_execution(data, job, user_define_job=False, country='SE', ebay_keys=None) :
	buckets = split_tuple(data)
	writing_threads = {}
	for bucket_count, bucket in enumerate(buckets) :
		if user_define_job :
			if ebay_keys is None :
				writing_threads[bucket_count] = threading.Thread(target=job, args=([bucket, country]))
			else :
				writing_threads[bucket_count] = threading.Thread(target=job, args=([bucket, ebay_keys, country]))
		else :
			if ebay_keys is None :
				writing_threads[bucket_count] = threading.Thread(target=iterate_over_bucket, args=([bucket, job, country]))
			else :
				writing_threads[bucket_count] = threading.Thread(target=iterate_over_bucket, args=([bucket, job, ebay_keys, country]))
		writing_threads[bucket_count].start()
	# Join all the threads
	for i, bucket in enumerate(buckets) :
		writing_threads[i].join()
