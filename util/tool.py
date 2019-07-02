# -*- coding: utf-8 -*-
import datetime as dt

"""
set string { ... } to list 
"""
def to_list(text):
    return text.replace('{','').replace('}','').split(',')

"""
convert year, month, day 
"""
def to_time(text):
    return dt.datetime.strptime(text.split(' ')[0], '%Y-%m-%d')