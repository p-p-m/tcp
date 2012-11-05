#coding: utf-8

import os
import doctors
import datetime
import random, glob



INBOX = u"C:/Program Files/Holter/Inbox"
DOCTORS = u"C:/Program Files/Holter/Inbox/Doctors"
ARCHIVE_PATH = r'\\MYBOOKLIVE\Public'
ENG_MONTH_NAMES = 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
XLS_HOLTERS_PATH = u'static/xls_holters'

def all_doctors():
	ALL_DOCTORS = []
	for path in glob.glob(os.path.join('doctors', '*')):
		ALL_DOCTORS.append(doctors.Doctor(load_path = path))
	return ALL_DOCTORS


def show_all_doctors():
        print 'Program init. Doctors:'
        for doctor, i in zip(all_doctors(), range(len(all_doctors()))) :
                print i+1, 'Doctor:', doctor.engname
                # print '\t', 'name:', doctor.name
                print '\t', 'working:', doctor.working
                print '\t', 'limit:', doctor.limit
                print '\t', 'stations:', doctor.stations
                print '\t', 'ablimit:', doctor.ablimit


# AV = doctors.Doctor(name = u'Алина Викторовна', engname = 'AV')
# AV.folder = os.path.join(DOCTORS, AV.name, _today_date())
# AV.working = True

# MR = doctors.Doctor(name = u'Михаил Русланович', engname = 'MR')
# MR.folder = os.path.join(DOCTORS, MR.name, _today_date())
# MR.working = False

# YV = doctors.Doctor(name = u'Юлия Владимировна', engname = 'YV')
# YV.folder = os.path.join(DOCTORS, YV.name, _today_date())
# YV.working = True
# YV.limit = 3
# YV.stations = [u'AB']
# # YV.ablimit = 2

# ON = doctors.Doctor(name = u'Ольга Николаевна', engname = 'ON')
# ON.folder = os.path.join(DOCTORS, ON.name, _today_date())
# ON.working = True
# ON.limit = 4
# ON.ablimit = 2

# ALL_DOCTORS = AV, MR, YV, ON
