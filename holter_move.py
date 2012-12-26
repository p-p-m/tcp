#coding: utf-8

from settings import all_doctors, INBOX, DOCTORS

import os
import sys
import glob
import datetime
import random
import shutil
import time
import msvcrt
import copy

from support.utf8_converter import setup_console
from logger import pprint

PROGRAM = False
next_doctor = None


def _today_date():
    date = datetime.datetime.now() + datetime.timedelta(0, 6 * 60 * 60)
    return date.strftime("%d.%m.%Y")


def _init_new_day():
    for doctor in all_doctors():
        prefolder = os.path.split(doctor.folder)[0]
        if os.path.split(doctor.folder)[1] != _today_date():
            pprint('init new day', _today_date())
            doctor.folder = os.path.join(prefolder, _today_date())
            doctor.save_doctor()


def _get_next_doctor(holter):
    doctors = [doctor for doctor in all_doctors() if doctor.is_holter_available(holter)]
    # print [doctor.engname for doctor in doctors]
    selected_doctor = doctors[0]
    for doctor in doctors:
        if doctor.holters_count() < selected_doctor.holters_count():
            selected_doctor = doctor
    min_doctors = [doctor for doctor in doctors if selected_doctor.holters_count == doctor.holters_count]
    return min_doctors[random.randint(0, len(min_doctors) - 1)]


def _move_holters(holters):
    global next_doctor
    if holters:
        pprint('moving holters at:', datetime.datetime.now().strftime("%d-%m %H:%M"))
    for holter in holters:
        if _reject_holter(holter):
            continue
        next_doctor = _get_next_doctor(holter)
        next_doctor.move_holter_to_folder(holter)


def _reject_holter(holter):
    moved_holters_names = _get_all_holters_in_folder(DOCTORS)
    if os.path.split(holter)[1].lower() in moved_holters_names:
        pprint('holter:', os.path.split(holter)[1], '>>> rejected')
        shutil.copy2(holter, os.path.join(INBOX, 'rejected'))
        os.remove(holter)
        return True
    else:
        return False


def _get_all_holters_in_folder(folder):
    holters = []
    for root, dirs, files in os.walk(folder):
        holters += [name.lower() for name in files if name.lower().endswith('.zhr')]
    return holters


def distribute_holters():
    holters = glob.glob(os.path.join(INBOX, '*.ZHR'))
    _init_new_day()
    _move_holters(holters)


def start_program(seconds):
    c = ''
    while c != 'q':
        if msvcrt.kbhit():
            c = msvcrt.getch()
        distribute_holters()
        time.sleep(seconds)

if __name__ == '__main__':
    setup_console()
    start_program(5.0)
    # print _get_all_holters_in_folder(DOCTORS)
