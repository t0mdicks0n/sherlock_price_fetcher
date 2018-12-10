import sys, os
import datetime

def print_exception(caller, exception) :
	# Get info on the exceotion
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(str(datetime.datetime.now()) + ": There was an exception from " + caller + ": " + str(exception))
	# Print what python stores in memory about the exception
	print(exc_type, fname, exc_tb.tb_lineno)