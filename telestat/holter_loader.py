#coding: utf-8
'''
Created on 24.09.2012

@author: Pavel

Gets holters from folders (constant FOLDERS) and stores them into file holters.xls
TODO: download folders pathes from file 
'''
import HolterWrapper

import os
import glob
import xlrd
import xlwt
from xlutils.copy import copy

HOLTER_COLUMNS = {'holter_name' : 5, 'holter_date' : 3, 'station' : 4, 'day' : 0, 'month' : 1, 'year' : 2,
     'patient_name' : 6, 'patient_birth_date' : 7, 'holter_path' : 8}
COLUMN_NAMES = [u'Дата', u"Код", u"Имя холтера", u"Имя пациента", u"Дата рождения", u"Путь к холтеру"]
FOLDERS = (r'\\MYBOOKLIVE\Public\2012\JAN', )

# def import_pathes ():
#     f = open(PATHFILE, 'rb')
#     return f.readline()


def read_holters(path):
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    holters = []
    for rownum in range(1, sh.nrows):
        holter = {}
        for value, name in zip(sh.row_values(rownum), COLUMN_NAMES):
            holter[name] = value
        holters.append(holter)
    return holters


def _get_existing_holters (path):
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    return sh.col_values(HOLTER_COLUMNS['holter_name'])[1:]


def _write_holter(sheet, row, holter):
    for key in holter:
        # print 'row = ', row, 'column = ', HOLTER_COLUMNS[key], 'key = ', key, 'value = ', holter[key]
        sheet.write(row, HOLTER_COLUMNS[key], holter[key])


def write_holters(holters, output):
    wb = xlrd.open_workbook(output)
    sheet = wb.sheet_by_index(0)
    copied_wb = copy(wb)
    csheet = copied_wb.get_sheet(0)
    
    write_row = len(sheet.col_values(2))
    for holter in holters:
        _write_holter(csheet, write_row, holter)
        write_row += 1

    del wb
    copied_wb.save(output)


def _get_all_holters_in_folder(folder):
    holters = []
    for root, dirs, files in os.walk(folder):
        holters += [os.path.join(root.lower(), name) for name in files if name.lower().endswith('.zhr')]
    return holters


def write_new_holters(folders, output):
    existing_holters = _get_existing_holters(output) if os.path.exists(output) else []
    newholter_pathes = []
    for pathes in [_get_all_holters_in_folder(folder) for folder in folders]:
        newholter_pathes += [path for path in pathes if not os.path.split(path)[1] in existing_holters]
    
    print 'naydeno', len(newholter_pathes), 'unikalnih holterov'

    holters = []
    if len(newholter_pathes): print 'schitivayu holtera:'
    for path, i in zip(newholter_pathes, range(len(newholter_pathes))):
        print 'holter (', i+1 ,':', len(newholter_pathes), ')', path
        holters.append(HolterWrapper.load_holter(path))

    if holters: 
        print 'Sohranyaem v', output
        write_holters(holters, output)


if __name__ == '__main__':
    # search_path = str(import_pathes())
    # search_path = r'\\MYBOOKLIVE\Public\2012\APR\*\*.ZHR'
    # pathes = glob.glob(search_path)
    print 'programa zapushena. Poisk unikalnih holterov...'
    write_new_holters(FOLDERS, 'holters.xls')

    # raw_input('Programa zavershila rabotu, nashmite lyubuyu knopku')
