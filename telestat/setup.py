#coding: utf-8
'''
Created on 24.09.2012

@author: Pavel
'''
from distutils.core import setup
import py2exe

setup(name='telestat',
      version='1.0',
      description='moves data from holter files(.ZHR) to xls files',
      author='Pavel Marchuk',
      author_email='marchukpavelp@gmail.com',
      py_modules = ['holter_loader', 'HolterWrapper'],
      console=['holter_loader.py']
     )
