#coding: utf-8

import os

def _get_holters_count(folder, current_month):
	holters_count = {}
	for root, dirs, files in os.walk(folder):
		for name in files:
			date = os.path.split(root)[1]
			if date.split
			if not date in holters_count: holters_count[date] = 0
			holters_count[date] += 1 
	return holters_count


if __name__ == '__main__':
	print _get_holters_count(os.path.join(r'\\MYBOOKLIVE','Public','2012','AUG'))