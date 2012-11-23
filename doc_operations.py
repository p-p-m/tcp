#coding: utf-8

import os
import datetime

from settings import all_doctors, DOCTORS
from holter_move import _today_date
import doctors

def create_doctor(form):
	doctor = doctors.Doctor(name = form['name'].decode('utf-8'), engname = form['engname'])
	docfolder = os.path.join(DOCTORS, doctor.name)
	doctor.folder = os.path.join(docfolder, _today_date())
	if not os.path.exists(docfolder): os.mkdir(docfolder)
	if not os.path.exists(doctor.folder): os.mkdir(doctor.folder)
	doctor.save_doctor()
	return doctor


def init_doctors_parameters(doctor, form):
	doctor.stations = [station.strip() for station in form['stations'].split(',') if station != u'']
	if 'limit' in form:
		if int(form['limitvalue']) < 0: raise ValueError
		doctor.limit = int(form['limitvalue'])
	else: doctor.limit = -1
	if 'ablimit' in form:
		if int(form['ablimitvalue']) < 0: raise ValueError
		doctor.ablimit = int(form['ablimitvalue'])
	else: doctor.ablimit = -1
	doctor.save_doctor()


def doctor_by_request(request):
	login = request.args.get('name', '')
	doctors = [doctor for doctor in all_doctors() if doctor.engname == login]
	return doctors[0] if doctors else None


def _holters_from_folder(folder):
	holters = os.listdir(folder)
	return [holter for holter in holters if holter.lower().endswith('.zhr')]


def last_holters(doctor, days_count):
	'''
	Returns doctors holters from last days, defined by days_count
	'''
	today = datetime.datetime.strptime(_today_date(), "%d.%m.%Y")
	predate_folder = os.path.split(doctor.folder)[0]
	holters = {}
	for i in xrange(days_count):
		date = today - datetime.timedelta(i, 0)
		holters_folder = os.path.join(predate_folder, date.strftime("%d.%m.%Y"))
		if os.path.exists(holters_folder):
			holters[date.strftime("%d.%m.%Y")] = _holters_from_folder(holters_folder)
	return holters


def delete_doctor(doctor):
	os.remove(os.path.join('doctors', doctor.engname))