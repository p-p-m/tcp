#coding: utf-8

import os
import doctors
import glob

ADMIN_PASSWORD = '12378956'
ACC_PASSWORD = 'stem79'

INBOX = u"C:/Program Files/Holter/Inbox"
DOCTORS = u"C:/Program Files/Holter/Inbox/Doctors"
ARCHIVE_PATH = r'\\MYBOOKLIVE\Public'
ENG_MONTH_NAMES = 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
XLS_HOLTERS_PATH = u'static/xls_holters'


def all_doctors():
    ALL_DOCTORS = []
    for path in glob.glob(os.path.join('doctors', '*')):
        ALL_DOCTORS.append(doctors.Doctor(load_path=path))
    return ALL_DOCTORS


def show_all_doctors():
    print 'Program init. Doctors:'
    for doctor, i in zip(all_doctors(), range(len(all_doctors()))):
        print i + 1, 'Doctor:', doctor.engname
        # print '\t', 'name:', doctor.name
        print '\t', 'working:', doctor.working
        print '\t', 'limit:', doctor.limit
        print '\t', 'stations:', doctor.stations
        print '\t', 'ablimit:', doctor.ablimit
