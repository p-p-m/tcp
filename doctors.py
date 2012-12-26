#coding: utf-8

import os
import os.path
import glob
import shutil, re
import datetime

from logger import pprint

class Doctor(object):

	def __init__(self, name = None, engname = None, password = None, folder = None, stations = [],
					load_path = None, limit = -1, working = True, ablimit = -1, unworking_dates = []):
		self._name = name
		self._engname = engname
		self._folder = folder
		self._stations = stations
		self._limit = limit
		self._working = working
		self._ablimit = ablimit
		self._unworking_dates = unworking_dates
		self._password = password
		if load_path: self.load_doctor(load_path)

	def name():
	    doc = "The name property."
	    def fget(self):
	        return self._name
	    def fset(self, value):
	        self._name = value
	    def fdel(self):
	        del self._name
	    return locals()
	name = property(**name())

	def engname():
	    doc = "The engname property."
	    def fget(self):
	        return self._engname
	    def fset(self, value):
	        self._engname = value
	    def fdel(self):
	        del self._engname
	    return locals()
	engname = property(**engname())

	def password():
	    doc = "The password property."
	    def fget(self):
	        return self._password
	    def fset(self, value):
	        self._password = value
	    def fdel(self):
	        del self._password
	    return locals()
	password = property(**password())

	def folder():
	    doc = "The folder property."
	    def fget(self):
	        return self._folder
	    def fset(self, value):
	        self._folder = value
	    def fdel(self):
	        del self._folder
	    return locals()
	folder = property(**folder())

	def limit():
	    doc = "The limit property."
	    def fget(self):
	        return self._limit
	    def fset(self, value):
	        self._limit = value
	    def fdel(self):
	        del self._limit
	    return locals()
	limit = property(**limit())

	def stations():
	    doc = "The stations property."
	    def fget(self):
	        return self._stations
	    def fset(self, value):
	        self._stations = value
	    def fdel(self):
	        del self._stations
	    return locals()
	stations = property(**stations())

	def working():
	    doc = "The working property."
	    def fget(self):
	    	date = datetime.datetime.strptime(os.path.split(self.folder)[1], '%d.%m.%Y')
	    	date = str(date.day) + '.' + str(date.month)
	        return not date in self.unworking_dates
	    def fset(self, value):
	    	raise Error('can`t set working - only from calendar')
	    return locals()
	working = property(**working())

	def ablimit():
	    doc = "The ablimit property."
	    def fget(self):
	        return self._ablimit
	    def fset(self, value):
	        self._ablimit = value
	    def fdel(self):
	        del self._ablimit
	    return locals()
	ablimit = property(**ablimit())

	def unworking_dates():
	    doc = "The unworking_dates property."
	    def fget(self):
	        return self._unworking_dates
	    def fset(self, value):
	        self._unworking_dates = value
	    def fdel(self):
	        del self._unworking_dates
	    return locals()
	unworking_dates = property(**unworking_dates())


	def formated_stations():
		def fget(self):
			return ','.join(self._stations)
		return locals()
	formated_stations = property(**formated_stations())


	def move_holter_to_folder(self, holter):
		if not os.path.isdir(self._folder):
			pprint('creating folder:', os.path.split(self._folder)[1], self._engname)
			os.mkdir(self._folder)
		print 'holter:', os.path.split(holter)[1], ' >>> ', os.path.split(self._folder)[1], self._engname
		shutil.copy2(holter, self._folder)
		os.remove(holter)


	def holters_count(self):
		return len(glob.glob(os.path.join(self._folder, '*.ZHR')))


	def is_holter_available(self, holter):
		# (_today_date().split('.')[0] + '.' + _today_date().split('.')[1]) in doctor.unworking_dates
		station = os.path.split(holter)[1][0:2]
		holters_in_folder = len(glob.glob(os.path.join(self._folder, '*.ZHR')))
		abholters_in_folder = len(glob.glob(os.path.join(self._folder, u'AB*.ZHR')))
		if not self.working: return False
		if station in self._stations: return False
		if self._limit != -1: 
			if holters_in_folder >= int(self._limit): return False
		if self._ablimit != -1 and station == u'AB': 
			if abholters_in_folder >= int(self._ablimit): return False
		return True


	def save_doctor(self):
		f = open(os.path.join('doctors', self._engname), 'wb')
		for d in self.__dict__:
			line = d + ':::' + str(self.__getattribute__(d)) + '$$$'
			f.write(line)
		f.close()


	def _load_list(self, value):
		list = []
		for part in value.split(','):
			strlist = re.findall('\'.*\'', part)
			strel = strlist[0][1:-1] if strlist else None
			if strel: list.append(strlist[0][1:-1].decode('unicode-escape'))
		return list


	def load_doctor(self, path):
		f = open(path, 'rb')
		elemets = f.read()[:-3].split('$$$')
		for element in elemets:
			name = element.split(':::')[0]
			value = element.split(':::')[1]
			if name in ('_stations', '_unworking_dates'):
				self.__setattr__(name, self._load_list(value))
			else:
				self.__setattr__(name, value.decode('utf-8'))
		self._limit = int(self._limit)
		self._ablimit = int(self._ablimit)
		self._working = True if self._working == 'True' else False
		f.close()
