#coding: utf-8
import functools

from flask import session, abort

from settings import all_doctors

def _check_doctor(login, password):
    for doctor in all_doctors():
        if doctor.engname == login and doctor.password == password:
            return doctor
    return False


def doctor_wrapper(function):
    '''
    decorator to check if doctor loggined
    '''
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if 'doctor' in session and _check_doctor(session['doctor'].engname, session['doctor'].password):
            return function(*args, **kwargs)
        else: abort(401)
    return wrapper


def doctor_loggining(login, password):
    '''
    if login and password is available writes them into session and returns true else returns False
    '''
    doctor = _check_doctor(login, password)
    if doctor:
        session['doctor'] = doctor
        return True
    else:
        return False