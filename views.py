#coding: utf-8
import sys
import datetime
import subprocess
import msvcrt
import os
import glob

from werkzeug import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for, abort, send_file, session
# from jinja2 import Environment, PackageLoader, environmentfilter
import calendar
import doc_operations

from settings import all_doctors, DOCTORS, show_all_doctors
from support.utf8_converter import setup_console
from tccalendar import get_monthes, move_to_archive, get_doctor_holters_count
from holter_move import _today_date
from telestat import HolterWrapper
import tclogin


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = 'C:\Program Files\Holter\Outbox'

# environment = app.create_jinja_environment()
#filter for holter data: using to show popup window with patient data on click on holters count


program_process = None
watch_process = None
first_program_start = True

DAYS_COUNT = 3


@app.route('/')
@tclogin.user_wrapper(groups=['admin'])
def first():
    global program_process
    global first_program_start
    global watch_process
    if not watch_process:
        watch_process = subprocess.Popen((sys.executable, 'logger.py'))
    if (request.args.get('start', '') and not program_process) or first_program_start:
        first_program_start = False
        print 'starting program_process'
        hm_parameters = (sys.executable, 'holter_move.py')
        program_process = subprocess.Popen(hm_parameters)
    if request.args.get('stop', '') and program_process:
        if program_process:
            print 'killing program_process'
            program_process.kill()
        program_process = None
    return render_template('first.html', doctors=all_doctors(), program_working=True if program_process else False)


@app.route('/processes/')
def processes():
    return render_template('processes: ' + ' '.join(str(arg) for arg in program_process))


@app.route('/doctor/', methods=['POST', 'GET'])
@tclogin.user_wrapper(groups=['admin'])
def doctor():
    '''
    changes doctors parameters or creates new doctor
    '''
    doctor = doc_operations.doctor_by_request(request)
    if request.method == 'POST':
        if not doctor:
            try:
                doctor = doc_operations.create_doctor(request.form)
                flash(u"Доктор успешно создан", 'normal')
                return redirect(url_for('first'))
            except:
                flash(u'Неправильно заполнены поля', 'error')
                return render_template('doctor.html', doctor=doctor)
        else:
            try:
                doc_operations.init_doctors_parameters(doctor, request.form)
                flash(u"Настройки успешно сохранены", 'normal')
                return redirect(url_for('doctor_control'))
            except:
                flash(u'Неправильно заполнен общий лимит или аб-лимит', 'error')
                return redirect(url_for('doctor') + '?name=' + doctor.engname)
    return render_template('doctor.html', doctor=doctor)


@app.route('/schedule/', methods=['POST', 'GET'])
@tclogin.user_wrapper(groups=['admin'])
def schedule():
    doctor = doc_operations.doctor_by_request(request)
    if request.method == 'POST':
        doctor.unworking_dates = [date for date in request.form]
        print doctor.unworking_dates
        doctor.save_doctor()
        flash(u"Расписание успешно сохранено", 'normal')
        return redirect(url_for('first'))
    monthes = get_monthes(doctor)
    return render_template('calendar.html', monthes=monthes, doctor=doctor)


@app.route('/archive/', methods=['POST', 'GET'])
@tclogin.user_wrapper(groups=['admin'])
def archive():
    if request.method == 'POST':
        try:
            move_to_archive(request.form['date'])
            flash(u"Перемещение в архив прошор успешно", 'normal')
        except ValueError:
            flash('Неправильный формат даты', 'error')
    return render_template('archive.html')


@app.route('/small-statistics/')
@tclogin.user_wrapper(groups=['admin', 'accountant'])
def small_statistics():
    doctor = doc_operations.doctor_by_request(request)
    doctors = all_doctors() if not doctor else [doctor]
    data = []
    today = datetime.datetime.strptime(_today_date(), ("%d.%m.%Y"))
    monthrange = calendar.monthrange(today.year, today.month)[1]
    #holters count for every day
    for doc in doctors:
        holters_count = get_doctor_holters_count(doc, DOCTORS, int(_today_date().split('.')[1]))
        for i in range(monthrange):
            if not i + 1 in holters_count:
                holters_count[i + 1] = -1
        # sum for all month (raw-sum):
        holters_sum = 0
        for hc in holters_count:
            if holters_count[hc] != -1:
                holters_sum += holters_count[hc]
        holters_count['sum'] = holters_sum
        data.append([doc.name, holters_count])
    #every day sum(column sum)
    if len(doctors) > 1:
        ed_sum = {}
        for day in holters_count:
            day_counts = [d[1][day] for d in data if d[1][day] != -1]
            ed_sum[day] = sum(day_counts)
        data.append(['Сумма за день', ed_sum])
    return render_template('small_statistics.html', data=data, monthrange=monthrange)


@app.template_filter('holters_data')
def _holters_data(doctor_and_day):
    '''
    This filter uses in small statistics to get holters data (patient name and holter name)
    '''
    #getting date
    day = doctor_and_day.split('$')[1]
    today_date = datetime.datetime.now()
    date = datetime.date(day=int(day), month=today_date.month, year=today_date.year)
    #getting doctor folder
    docfolder = doctor_and_day.split('$')[0].decode('utf-8')
    if docfolder == u'Сумма за день':  # in this case we need to show all doctros
        holters_data = ''
        for doctor in all_doctors():
            holters_data += _holter_data_by_doctor(doctor.name, date, doctor_name=doctor.name)
        header = '<tr><th>Доктор</th><th>Холтер</th><th>ФИО пациента</th></tr>'
    else:  # getting holters for one choosen doctor
        holters_data = _holter_data_by_doctor(docfolder, date)
        header = '<tr><th>Холтер</th><th>ФИО пациента</th><th>'
    return header + holters_data


def _holter_data_by_doctor(docfolder, date, doctor_name=None):
    '''
    Takes holters data from given docfolder and given date. Returns rows for html table.
    If doctor_name is given adds column with doctor name to rows.
    '''
    holters_data = []
    for path in glob.glob(os.path.join(DOCTORS, docfolder, date.strftime('%d.%m.%Y'), '*.zhr')):
        holter = HolterWrapper.load_holter(path)
        if doctor_name:
            holters_data.append('<td>' + '</td><td>'.join([doctor_name, holter['holter_name'], holter['patient_name']]) + '</td>')
        else:
            holters_data.append('<td>' + '</td><td>'.join([holter['holter_name'], holter['patient_name']]) + '</td>')
    return '<tr>' + '</tr><tr>'.join(holters_data) + '</tr>'


@app.route('/doctor_control/<action>/')
@tclogin.user_wrapper(groups=['admin'])
def doctor_action(action):
    '''
    Deletes doctor or creates new
    '''
    if action == 'delete':
        doctor = doc_operations.doctor_by_request(request)
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
    return render_template('doctor_control.html', doctors=all_doctors())


#*******************************************************************************************************#
#*************************************   doctor part   *************************************************#
#*******************************************************************************************************#


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = False
        form = request.form
        user = tclogin.loggining(form['login'], form['password'])
        redirect_pages = {
                'admin': url_for('first'),
                'doctor': url_for('doctor_personal'),
                'accountant': url_for('big_statistics'),
            }
        if user:
            session['user'] = user
            return redirect(redirect_pages[user.group])
        else:
            return render_template('login.html', error='O_o неправильный пароль! ...пожалуйста введите заново')
    else:
        return render_template('login.html')


@app.route('/doctor_personal/', methods=['POST', 'GET'])
@tclogin.user_wrapper(group='doctor')
def doctor_personal():
    '''
    Shows doctor main page if doctor is in session
    '''
    doctor = doc_operations.doctor_by_login(session['user'].login)
    if not doctor:
        abort(404)
    if request.method == 'POST' and 'file' in request.files:
        upload_status = _upload_file(request.files['file'])
        if upload_status:
            flash(upload_status)
        else:
            print 'file not uploaded'
            flash('Ваш файл незагружен. Допустимое разширение отчета .zpt', 'error')
    last_holters = doc_operations.last_holters(doctor, DAYS_COUNT)
    if request.args.get('download_holter', ''):
        return _send_holter(request, doctor)
    return render_template('doctor_personal.html', holters=last_holters)


def _send_holter(request, doctor):
    last_holters = doc_operations.last_holters(doctor, DAYS_COUNT)
    all_holters = []
    for h in last_holters.values():
        all_holters += h
    holter = request.args.get('download_holter', '')
    holter_date = request.args.get('holter_date', '')
    prefolder = os.path.split(doctor.folder)[0]
    if holter and holter_date:
        if holter in all_holters:
            return send_file(os.path.join(prefolder, holter_date, holter), as_attachment=True)
        else:
            flash("Немогу найти такого холтера. Может его уже нет?", 'error')
    return render_template('doctor_personal.html', holters=last_holters)


def _upload_file(file):
    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Файл ' + filename + ' успешно сохранен'
    return False


def _allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['zpt'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#*******************************************************************************************************#
#*************************************   accountant part   *********************************************#
#*******************************************************************************************************#


@app.route('/big_statistics/', methods=['POST', 'GET'])
@tclogin.user_wrapper(group='accountant')
def big_statistics():
    return render_template('big_statistics.html')


#*******************************************************************************************************#
#*************************************   error handlers   **********************************************#
#*******************************************************************************************************#


@app.errorhandler(401)
def page_not_found(error):
    return render_template('unauthorized.html'), 404


if __name__ == '__main__':
    setup_console()
    # global environment
    # environment.filters['holters_data'] = holters_data
    # print environment.get_template('small_statistics.html')
    # print environment.filters['holters_data']
    show_all_doctors()
    app.run(debug=True)
    c = ''
    while c != 'q':
        if msvcrt.kbhit():
            c = msvcrt.getch()
