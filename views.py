#coding: utf-8
from sys import executable

from flask import Flask, render_template, request, flash, redirect, url_for
import datetime, subprocess, msvcrt, os, calendar
import doctors, doc_operations

from settings import all_doctors, DOCTORS, show_all_doctors
from support.utf8_converter import setup_console
from tccalendar import get_monthes, move_to_archive, MONTH_NAMES, get_doctor_holters_count
from holter_move import _today_date
import telestat.big_statistic as bs 


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

program_process = None
first_program_start = True


@app.route('/')
def first():
	global program_process
	global first_program_start
	if (request.args.get('start', '') and not program_process) or first_program_start:
		first_program_start = False
		hm_parameters = (executable, 'holter_move.py')
		program_process = subprocess.Popen(hm_parameters)
	if request.args.get('stop', '') and program_process:
		program_process.kill()
		program_process = None
	return render_template('first.html', doctors = all_doctors(), program_working = True if program_process else False) 


@app.route('/doctor/', methods = ['POST', 'GET'])
def doctor():
	'''
	changes doctors parameters or creates new doctor
	'''
	doctor = doc_operations.get_doctor_by_login(request)
	if request.method == 'POST':
		if not doctor: 
			try:
				doctor = doc_operations.create_doctor(request.form)
				flash(u"Доктор успешно создан", 'normal')
				return redirect(url_for('first'))
			except:
				flash(u'Неправильно заполнены поля', 'error')
				return render_template('doctor.html', doctor = doctor)
		else:
			try: 
				doc_operations.init_doctors_parameters(doctor, request.form)
				flash(u"Настройки успешно сохранены", 'normal')
				return redirect(url_for('doctor_control'))
			except:
				flash(u'Неправильно заполнен общий лимит или аб-лимит', 'error')
				return redirect(url_for('doctor') + '?name=' + doctor.engname)
	return render_template('doctor.html', doctor = doctor)


@app.route('/schedule/', methods = ['POST', 'GET'])
def schedule():
	doctor = doc_operations.get_doctor_by_login(request)
	if request.method == 'POST':
		doctor.unworking_dates = [date for date in request.form]
		print doctor.unworking_dates
		doctor.save_doctor()
		flash(u"Расписание успешно сохранено", 'normal')
		return redirect(url_for('first'))
	monthes = get_monthes(doctor)
	return render_template('calendar.html', monthes = monthes, doctor = doctor)


@app.route('/archive/', methods = ['POST', 'GET'])
def archive():
	if request.method == 'POST':
		try:
			move_to_archive(request.form['date'])
			flash(u"Перемещение в архив прошор успешно", 'normal')
		except ValueError as er:
			flash('Неправильный формат даты', 'error')
	return render_template('archive.html')


@app.route('/small-statistics/')
def small_statistics():
	doctor = doc_operations.get_doctor_by_login(request)
	doctors = all_doctors() if not doctor else [doctor]
	data = []
	today = datetime.datetime.strptime(_today_date(), ("%d.%m.%Y"))
	monthrange = calendar.monthrange(today.year, today.month)[1]
	#holters count for every day
	for doc in doctors:
		holters_count = get_doctor_holters_count(doc, DOCTORS, int(_today_date().split('.')[1]))
		for i in range(monthrange):
			if not i+1 in holters_count: 
				holters_count[i+1] = -1
		# sum for all month (raw-sum):
		holters_sum = 0
		for hc in holters_count:
			if holters_count[hc] != -1: holters_sum += holters_count[hc]
		holters_count['sum'] = holters_sum
		data.append([doc.name, holters_count])
	#every day sum(column sum)
	if len(doctors) > 1:
		ed_sum = {}
		for day in holters_count:
			day_counts = [d[1][day] for d in data if d[1][day] != -1]
			ed_sum[day] = sum(day_counts)
		data.append(['Сумма за день', ed_sum])
	return render_template('small_statistics.html', data = data, monthrange = monthrange)


@app.route('/doctor_control/<action>/')
def doctor_action(action):
	'''
	deletes doctor or creates new
	'''
	if action == 'delete':
		doctor = doc_operations.get_doctor_by_login(request)
		if not doctor:
			flash("Неправильное имя доктора", 'error')
			return redirect(url_for('doctor_control'))
		doc_operations.delete_doctor(doctor)
		flash('Доктор успешно удален', 'normal')
		return redirect(url_for('doctor_control'))
	if action == 'create':
		return redirect(url_for('doctor'))


@app.route('/doctor_control/')
def doctor_control():
	return render_template('doctor_control.html', doctors = all_doctors())
	

if __name__ == '__main__':
	setup_console()
	show_all_doctors()
	app.run(debug = True)
	c = ''
	while c != 'q':
		if msvcrt.kbhit(): c = msvcrt.getch()

	# print bs.get_month_holters(2012,4)

	# print get_doctor_holters_count(all_doctors()[1], DOCTORS, int(_today_date().split('.')[1]))
