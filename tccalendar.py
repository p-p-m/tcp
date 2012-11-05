#coding: utf-8

import datetime, calendar, os, glob, shutil
from settings import DOCTORS, INBOX

MONTH_NAMES = 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'


def get_monthes(doctor):
	today = datetime.date.today()
	# print today.month
	# print (today.month + 1) % 12
	next_month = today.month + 1 if today.month != 12 else 1
	days = [today, datetime.date(today.year, next_month, 1)]

	monthes = []
	for day in days:
		month = {}
		month_data = _get_html_month(day, unworking_dates = doctor.unworking_dates)
		month['data'] = month_data
		month['name'] = MONTH_NAMES[day.month - 1]
		month['weeks_range'] = range(len(month_data) / 7)
		monthes.append(month)
	return monthes


def _get_html_month(today, unworking_dates = []):
	first_weekday = datetime.date.weekday(datetime.date(today.year, today.month, 1))
	last_day= calendar.monthrange(today.year,today.month)[1]
	html_month = []
	day = 1
	for i in range(6*7):
		if i < first_weekday or day > last_day:
			html_month.append({'type' : 'empty'})
			continue
		date = str(day) + '.' + str(today.month)
		if day < today.day:
			html_month.append({'type' : 'passive', 'value' : day, 'fullvalue' : date})
			day += 1
			continue
		if date in unworking_dates:
			html_month.append({'type' : 'checked', 'value' : day, 'fullvalue' : date})
			day += 1
			continue
		if day <= last_day:
			html_month.append({'type' : 'unchecked', 'value' : day, 'fullvalue' : date})
			day += 1

	if html_month[-7]['type'] == 'empty': html_month = html_month[:-7]
	return html_month


def __move_folder (folder):
    # print 'coping folder:', folder
    folder_name = os.path.split(folder)[1]
    new_folder = os.path.join(INBOX, 'archive', folder_name)
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)
    for holter_path in glob.glob(os.path.join(folder, u'*.ZHR')):
        shutil.copy2(holter_path, new_folder)
        # print holter_path, '>>>', new_folder
        os.remove(holter_path)

    print 'folder copied'


def move_to_archive(date):
    for folder in glob.glob(os.path.join(DOCTORS, u'*', u'*')):
        if datetime.datetime.strptime(os.path.split(folder)[1], '%d.%m.%Y') < \
                                        datetime.datetime.strptime(date, '%d.%m.%Y'):
            __move_folder(folder)
            # print folder
            shutil.rmtree(folder)
    print 'moving complete.'


def _get_holters_count(folder, current_month):
	holters_count = {}
	for root, dirs, files in os.walk(folder):
		for directory in dirs:
			if int(directory.split('.')[1]) == current_month and not int(directory.split('.')[0]) in holters_count:
				holters_count[int(directory.split('.')[0])] = 0
		for name in files:
			if name.lower().endswith('.zhr'):
				date = os.path.split(root)[1]
				if int(date.split('.')[1]) == current_month:
					day = int(date.split('.')[0])
					if not day in holters_count: holters_count[day] = 0
					holters_count[day] += 1 
	return holters_count


def get_doctor_holters_count(doctor, folder, current_month):
	assert doctor.name in os.listdir(folder), 'no doctor folder while counting holters for small statistics'
	findfolder = os.path.join(folder, doctor.name)
	return _get_holters_count(findfolder, current_month)
	
