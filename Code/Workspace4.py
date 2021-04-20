# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:51:28 2021

@author: BKG
"""
from pathlib import Path
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid
import PySimpleGUI as sg
import re

def main():
    print()
    values_page_1 = text_new_alumni_p1()
    print(values_page_1)
    
    
def text_new_alumni_p1():    
    frame_last_name = [[sg.Input(key='last')]]
    
    frame_first_name = [[sg.Input(key='first')]]
    
    frame_core_student = [[sg.Radio('Yes', 'CORE', key='core_yes'), 
                          sg.Radio('No', 'CORE', key='core_no', default=True)]]
    
    frame_grad_year = [[sg.Input(key='grad_year', size=(13,1),
                                 change_submits=True, do_not_clear=True),
                       sg.T('', key='error_grad_year', text_color='purple', size=(25,1))]]
    
    frame_phone_number = [[sg.In(key='phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True), 
                           sg.T('-', pad=(0,0)),
                           sg.In(key='phone2', size=(4,1), 
                                 change_submits=True, do_not_clear=True), 
                           sg.T('-', pad=(0,0)),
                           sg.In(key='phone3', size=(5,1), 
                                 change_submits=True, do_not_clear=True)]]
    
    frame_birthday = [[sg.In(key='bday_month', size=(3,1),
                             change_submits=True, do_not_clear=True),
                       sg.T('-', pad=(0,0)),
                       sg.In(key='bday_day', size=(3,1),
                             change_submits=True, do_not_clear=True),
                       sg.T('-', pad=(0,0)),
                       sg.In(key='bday_year', size=(5,1),
                             change_submits=True, do_not_clear=True),
                       sg.T('', key='error_bday', text_color='purple', size=(25,2))]]
    
    layout = [[sg.Text('New Alumni - Page 1')],
          [sg.Frame('Last Name', frame_last_name)],
          [sg.Frame('First Name', frame_first_name)],
          [sg.Frame('CORE Student?', frame_core_student)],
          
          [sg.Frame('Graduation Year', frame_grad_year)],
          [sg.Frame('Phone Number', frame_phone_number)],
          [sg.Frame('Birthday (mm-dd-yyyy)', frame_birthday)],
          [sg.OK(), sg.Cancel()] ]

    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event, values = window.read()

        if event in ('OK', 'Cancel', sg.WIN_CLOSED):
            break
        
### REGEX BLOCK ###
        if event in ('grad_year', 'phone1', 'phone2', 'phone3', 'bday_month', 'bday_day', 'bday_year'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))
            
        if event == 'grad_year' and len(window[event].Get()) >= 4:
            if not re.match('^20[0-4]{1}\d{1}$', window[event].Get()):
                window['error_grad_year'].Update('Please enter a valid year.')
                window['grad_year'].Widget.configure(highlightcolor='red', highlightthickness=2)
            else:
                window['error_grad_year'].Update('')
                window['grad_year'].Widget.configure(highlightcolor='white')
                window['phone1'].SetFocus()
                
        if event == 'bday_month':
            if not re.match('^0[1-9]|1[0-2]$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid month\n(e.g. Feb = 02).')
                window['bday_month'].Widget.configure(highlightcolor='red', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                window['bday_day'].SetFocus()
                
        if event == 'bday_day' and len(window[event].Get()) >= 1:
            if not re.match('^0[1-9]|1[0-9]|2[0-9]|3[0-1]$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid day\n(e.g. 3rd of month = 03).')
                window['bday_month'].Widget.configure(highlightcolor='red', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                window['bday_year'].SetFocus()
                
        if event == 'bday_year' and len(window[event].Get()) >= 1:
            if not re.match('^19\d{2}|20[0-4]{1}\d{1}$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid year\n(e.g. 1999.')
                window['bday_month'].Widget.configure(highlightcolor='red', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                
### END REGEX BLOCK ###

### SWITCH FOCUS BLOCK ###

        if event == 'phone1' and len(window[event].Get()) == 3:
            window['phone2'].SetFocus()
        if event == 'phone2' and len(window[event].Get()) == 3:
            window['phone3'].SetFocus()
        if event == 'phone3' and len(window[event].Get()) == 4:
            window['bday_month'].SetFocus()

    window.close()

    return values

def text_new_alumni_p2():
    frame_gender = [[sg.Radio('Female', 'gender', key='gender_female', default=True), 
                     sg.Radio('Male', 'gender', key='gender_male')]]
    frame_street_ad = [[sg.Input(key='street_address')]]
    frame_city = [[sg.Radio('Pittsburgh', 'city', key='city_pgh', default=True),
                   sg.Radio('Other', 'city', key='city_other')]]




def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection

    '''
    try:
        connection = sqlite3.connect('Data\\UIF_Alumni_DB.db')
    except Error:
        print(Error)
    return connection



if __name__ == "__main__":
    main()