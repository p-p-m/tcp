#coding: utf-8
'''
This module provides login checking for doctors, admin and acounter
'''
import functools

from flask import session, abort

from settings import all_doctors, ADMIN_PASSWORD, ACC_PASSWORD


class User (object):

    def __init__(self, login, password, group):
        self.login = login
        self.password = password
        self.group = group


def all_users():
    doctors = [User(d.engname, d.password, 'doctor') for d in all_doctors()]
    admin = User('admin', ADMIN_PASSWORD, 'admin')
    accountant = User('acc', ACC_PASSWORD, 'accountant')
    return doctors + [admin, accountant]


def _check_user(login, password):
    for user in all_users():
        if user.login == login and user.password == password:
            return user
    else:
        return None


def user_wrapper(groups=None):
    '''
    Decorator to check if user loggined
    '''
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            if not 'user'in session:
                abort(401)
            user = _check_user(session['user'].login, session['user'].password)
            if not user:
                abort(401)
            if groups and not user.group in groups:
                abort(401)

            return function(*args, **kwargs)
        return wrapper
    return decorator


def loggining(login, password):
    '''
    If login and password is available writes them into session and returns true else returns False
    '''
    user = _check_user(login, password)
    if user:
        session['user'] = user
        return user
    else:
        return False
