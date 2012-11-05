#coding: utf-8

import os
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


def get_doctor_by_login(request):
	login = request.args.get('name', '')
	doctors = [doctor for doctor in all_doctors() if doctor.engname == login]
	return doctors[0] if doctors else None


def delete_doctor(doctor):
	os.remove(os.path.join('doctors', doctor.engname))