#coding: utf-8
'''
this module prepares information for web-page
'''
import os

from settings import ENG_MONTH_NAMES, ARCHIVE_PATH, DOCTORS, XLS_HOLTERS_PATH
import holter_loader as loader



# def _get_holters_in_folder(folder):
# 	holters = []
# 	for root, dirs, files in os.walk(folder):
# 		holters += [os.path.join(root, name.lower()) for name in files if name.lower().endswith('.zhr')]
# 	return holters

# #month between 0 and 11
# def get_month_holters(year, month):
# 	holters = []
# 	xls_file_path = os.path.join(XLS_HOLTERS_PATH, str(month) + '.' + str(year) + '.xls')
# 	#looking in directories:
# 	print 'name :', ENG_MONTH_NAMES[4]
# 	print (os.path.join(ARCHIVE_PATH, str(year), ENG_MONTH_NAMES[month]), DOCTORS)
# 	for path in (os.path.join(ARCHIVE_PATH, str(year), ENG_MONTH_NAMES[month]), DOCTORS):
# 		if os.path.exists(path):
# 			loader.write_new_holters(_get_holters_in_folder(path), xls_file_path)
# 			holters += loader.read_holters(xls_file_path)
# 	return holters



