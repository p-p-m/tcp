#coding: utf-8
'''
Created on 20.08.2012

@author: Telecardio1
'''

import os.path
import re
from datetime import datetime
# from ..settings import all_doctors


SMALL_LETTER_BEGIN = 224
BIG_LETTER_BEGIN = 192
ALPHABET = u'абвгдежзийклмнопрстуфхцчшщъыьэюя'


def _to_rus(code):
    code = int(code, base=16)
    if code in range(SMALL_LETTER_BEGIN, SMALL_LETTER_BEGIN + len(ALPHABET)):
        return ALPHABET[code - SMALL_LETTER_BEGIN]
    if code in range(BIG_LETTER_BEGIN, BIG_LETTER_BEGIN + len(ALPHABET)):
        return ALPHABET[code - BIG_LETTER_BEGIN].upper()
    return ' '


def load_holter(path):
    holter_name = os.path.split(path)[1]
    holter_date = os.path.split(os.path.split(path)[0])[1]
    try:
        holter_date = datetime.strptime(holter_date, '%d.%m.%Y')
        hday, hmonth, hyear = str(holter_date.day), str(holter_date.month), str(holter_date.year)
    except ValueError:
        holter_date = 'unknown'
        hday, hmonth, hyear = ['?'] * 3

    station_code = holter_name[:2]
    text = open(path, mode='rb').read(6000)
    try:
        name_conteiner = re.search(station_code + '.*[Digitrak Plus, Philips]s', text, re.DOTALL).group(0).split(')')[-1]
        patient_name = ''
        for c in name_conteiner:
            c = _to_rus(c.encode('hex'))
            patient_name = patient_name + c
        patient_name = patient_name.replace(u'Регистратор', '')
        birth_date = re.search('\\' + '\\'.join('dd.dd.dddd'), text).group(0)
    except AttributeError:
        patient_name = '???'
        birth_date = 'unknown'

    try:
        birth_date = datetime.strptime(birth_date, '%d.%m.%Y').strftime('%d.%m.%Y')
    except:
        print 'Warning: wrong patient_date', birth_date
        birth_date = 'unknown'

    return {
        'holter_name': holter_name,
        'holter_date': holter_date if isinstance(holter_date, str) else holter_date.strftime('%d.%m.%Y'),
        'holter_path': path,
        'patient_name': patient_name.strip(),
        'patient_birth_date': birth_date,
        'station': station_code,
        'day': hday,
        'month': hmonth,
        'year': hyear
    }
