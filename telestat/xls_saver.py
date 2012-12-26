#coding: utf-8
'''
Created on 24.09.2012

@author: Pavel
'''
import HolterWrapper

import os
import glob
import xlrd
import xlwt
from xlutils.copy import copy

HOLTERSFILE = 'holters.xls'
PATHFILE = 'path.txt'
HOLTER_COLUMNS = {'holter_name' : 2, 'holter_date' : 0, 'station' : 1,
     'patient_name' : 3, 'patient_birth_date' : 4, 'holter_path' : 5}
COLUMN_NAMES = [u'Дата', u"Код", u"Имя холтера", u"Имя пациента", u"Дата рождения", u"Путь к холтеру"]


def import_pathes ():
    f = open(PATHFILE, 'rb')
    return f.readline()


def get_existing_holters ():
    wb = xlrd.open_workbook(HOLTERSFILE)
    sh = wb.sheet_by_index(0)
    return sh.col_values(2)[1:]

existing_holters = get_existing_holters()

def _write_holter(sheet, row, holter):
    for key in holter:
        # print 'row = ', row, 'column = ', HOLTER_COLUMNS[key], 'key = ', key, 'value = ', holter[key]
        sheet.write(row, HOLTER_COLUMNS[key], holter[key])


def write_holters(holters):
    wb = xlrd.open_workbook(HOLTERSFILE)
    sheet = wb.sheet_by_index(0)
    copied_wb = copy(wb)
    csheet = copied_wb.get_sheet(0)
    
    write_row = len(sheet.col_values(2))
    for holter in holters:
        _write_holter(csheet, write_row, holter)
        write_row += 1

    del wb
    copied_wb.save(HOLTERSFILE)
    

if __name__ == '__main__':
    # search_path = str(import_pathes())
    search_path = r'\\MYBOOKLIVE\Public\2012\*\*\*.ZHR'
    print 'smotrim holtera v papke:', search_path
    pathes = glob.glob(search_path)
    existing_holters = get_existing_holters()
    newholter_pathes = [path for path in pathes if not os.path.split(path)[1] in existing_holters]
    print 'naydeno', len(newholter_pathes), 'unikalnih holterov'

    holters = []
    if len(newholter_pathes): print 'schitivayu holtera:'
    for path, i in zip(newholter_pathes, range(len(newholter_pathes))):
        print 'holter (', i+1 ,':', len(newholter_pathes), ')', path
        holters.append(HolterWrapper.load_holter(path))


    if holters: 
        print 'Sohranyaem v', HOLTERSFILE
        write_holters(holters)

    raw_input('Programa zavershila rabotu, nashmite lyubuyu knopku')
