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

    values_page_1 = None
    values_page_2 = None
    values_page_3 = None
    values_page_4 = None
    values_page_5 = None

    values_page_1 = text_new_alumni_p1()
    if values_page_1 != None:
        values_page_2 = text_new_alumni_p2()
    if values_page_2 != None:
        values_page_3 = text_new_alumni_p3()
    if values_page_3 != None:
        values_page_4 = text_new_alumni_p4()
    if values_page_4 != None:
        values_page_5 = text_new_alumni_p5()

    print(values_page_1)
    print(values_page_2)
    print(values_page_3)
    print(values_page_4)
    print(values_page_5)

def text_new_alumni_p1():
    frame_last_name = [[sg.Input(key='last')]]

    frame_first_name = [[sg.Input(key='first')]]

    frame_core_student = [[sg.Radio('Yes', 'CORE', key='core_yes'),
                          sg.Radio('No', 'CORE', key='core_no', default=True)]]

    frame_grad_year = [[sg.Input(key='grad_year', size=(13,1),
                                 change_submits=True, do_not_clear=True),
                       sg.T('', key='error_grad_year', text_color='purple', size=(26,1))]]

    frame_phone_number = [[sg.In(key='phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='phone2', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='phone3', size=(5,1),
                                 change_submits=True, do_not_clear=True)]]

    frame_email = [[sg.In(key='email')]]

    layout = [[sg.Text('New Alumni - Page 1')],
          [sg.Frame('Last Name', frame_last_name)],
          [sg.Frame('First Name', frame_first_name)],
          [sg.Frame('CORE Student?', frame_core_student)],

          [sg.Frame('Graduation Year', frame_grad_year)],
          [sg.Frame('Phone Number', frame_phone_number)],
          [sg.Frame('Email', frame_email)],
          [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()] ]

    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break

        if event == 'next_page':
            break

        if event in ('grad_year', 'phone1', 'phone2', 'phone3'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'grad_year' and len(window[event].Get()) >= 1:
            if not re.match('^20[0-4]{1}\d{1}$', window[event].Get()):
                window['error_grad_year'].Update('Please enter a valid graduation year.')
                window['grad_year'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_grad_year'].Update('')
                window['grad_year'].Widget.configure(highlightcolor='white')
                window['phone1'].SetFocus()

        if event == 'phone1' and len(window[event].Get()) == 3:
            window['phone2'].SetFocus()
        if event == 'phone2' and len(window[event].Get()) == 3:
            window['phone3'].SetFocus()
        if event == 'phone3' and len(window[event].Get()) == 4:
            window['email'].SetFocus()

    window.close()

    return values

def text_new_alumni_p2():
    frame_birthday = [[sg.In(key='bday_month', size=(3,1),
                         change_submits=True, do_not_clear=True),
                   sg.T('-', pad=(0,0)),
                   sg.In(key='bday_day', size=(3,1),
                         change_submits=True, do_not_clear=True),
                   sg.T('-', pad=(0,0)),
                   sg.In(key='bday_year', size=(5,1),
                         change_submits=True, do_not_clear=True),
                   sg.T('', key='error_bday', text_color='purple', size=(25,2))]]

    frame_gender = [[sg.Radio('Female', 'gender', key='gender_female', default=True),
                     sg.Radio('Male', 'gender', key='gender_male')]]

    frame_street_ad = [[sg.In(key='street_address', size=(49,1))]]

    frame_city = [[sg.Radio('Pittsburgh', 'city', key='city_pgh', default=True),
                   sg.Radio('Other', 'city', key='city_other', enable_events=True),
                   sg.In(key='city_input', size=(25,1))]]

    frame_state = [[sg.Radio('Pennsylvania', 'state', key='state_pa', default=True),
                    sg.Radio('Other', 'state', key='state_other', enable_events=True),
                    sg.In(key='state_input', size=(23,1))]]

    frame_zipcode = [[sg.In(key='zipcode', size=(6,1),
                            change_submits=True, do_not_clear=True),
                      sg.T('', key='error_zipcode', text_color='purple', size=(36,2))]]


    layout = [[sg.T('New Alumni - Page 2')],
              [sg.Frame('Birthday (mm-dd-yyyy)', frame_birthday)],
              [sg.Frame('Gender', frame_gender)],
              [sg.Frame('Street Address', frame_street_ad)],
              [sg.Frame('City', frame_city)],
              [sg.Frame('State', frame_state)],
              [sg.Frame('Zipcode', frame_zipcode)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
            break

        if event == 'city_other':
            window['city_input'].SetFocus()
        if event == 'state_other':
            window['state_input'].SetFocus()

        if event in ('bday_month', 'bday_day', 'bday_year', 'zipcode'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'bday_month' and len(window[event].Get()) >= 1:
            if not re.match('^0[1-9]|1[0-2]$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid month\n(e.g. Feb = 02).')
                window['bday_month'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                window['bday_day'].SetFocus()

        if event == 'bday_day' and len(window[event].Get()) >= 1:
            if not re.match('^0[1-9]|1[0-9]|2[0-9]|3[0-1]$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid day\n(e.g. 3rd of month = 03).')
                window['bday_month'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                window['bday_year'].SetFocus()

        if event == 'bday_year' and len(window[event].Get()) >= 1:
            if not re.match('^19\d{2}|20[0-4]{1}\d{1}$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid year\n(e.g. 1999.')
                window['bday_month'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')

        if event == 'zipcode' and len(window[event].Get()) >= 1:
            if not re.match('^\d{5}$', window[event].Get()):
                window['error_zipcode'].Update('Please enter a 5 digit zipcode\n(e.g. 15212).')
                window['zipcode'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_zipcode'].Update('')
                window['zipcode'].Widget.configure(highlightcolor='white')


    window.close()

    return values


def text_new_alumni_p3():
    frame_church = [[sg.Radio('ACAC', 'church', key='church_acac', enable_events=True),
                     sg.Radio('None', 'church', key='church_none', enable_events=True)],
                     [sg.Radio('Other', 'church', key='church_other', enable_events=True),
                      sg.In(key='church_input')]]

    frame_highschool = [[sg.In(key='highschool', size=(55,1))]]

    frame_college = [[sg.In(key='college', size=(55,1))]]

    frame_job = [[sg.In(key='job', size=(55,1))]]

    frame_health = [[sg.In(key='health', size=(55,1))]]


    layout = [[sg.T('New Alumni - Page 3')],
              [sg.Frame('Church Affiliation', frame_church)],
              [sg.Frame('Highschool', frame_highschool)],
              [sg.Frame('College', frame_college)],
              [sg.Frame('Occupation', frame_job)],
              [sg.Frame('Special Health Concerns', frame_health)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
            break

        if event in ('church_acac', 'church_none'):
            window['highschool'].SetFocus()

        if event == 'church_other':
            window['church_input'].SetFocus()

    window.close()

    return values


def text_new_alumni_p4():
    frame_parent = [[sg.In(key='parent')]]
    frame_parent_phone = [[sg.In(key='parent_phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='parent_phone2', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='parent_phone3', size=(5,1),
                                 change_submits=True, do_not_clear=True)]]
    frame_parent_email = [[sg.In(key='parent_email')]]
    frame_emergency_contact = [[sg.In(key='e_contact')],
                               [sg.Checkbox('Use Parent/Guardian name from above',
                                            key='e_parent',
                                            enable_events=True)]]
    frame_emergency_phone = [[sg.In(key='e_phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='e_phone2', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='e_phone3', size=(5,1),
                                 change_submits=True, do_not_clear=True)],
                             [sg.Checkbox('Use Parent/Guardian phone number from above',
                                          key='e_number',
                                          enable_events=True)]]

    layout = [[sg.T('New Alumni - Page 4')],
              [sg.Frame('Parent/Guardian Full Name', frame_parent)],
              [sg.Frame('Parent/Guardian Phone Number', frame_parent_phone)],
              [sg.Frame('Parent/Guardian Email', frame_parent_email)],
              [sg.Frame('Emergency Contact Full Name', frame_emergency_contact)],
              [sg.Frame('Emergency Contact Phone Number', frame_emergency_phone)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
            break

        if event in ('parent_phone1', 'parent_phone2', 'parent_phone3',
                     'e_phone1', 'e_phone2', 'e_phone3'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'e_parent':
            window['e_contact'].Update(values['parent'])
        if event == 'e_number':
            window['e_phone1'].Update(values['parent_phone1'])
            window['e_phone2'].Update(values['parent_phone2'])
            window['e_phone3'].Update(values['parent_phone3'])

        if event == 'parent_phone1' and len(window[event].Get()) == 3:
            window['parent_phone2'].SetFocus()
        if event == 'parent_phone2' and len(window[event].Get()) == 3:
            window['parent_phone3'].SetFocus()
        if event == 'parent_phone3' and len(window[event].Get()) == 4:
            window['parent_email'].SetFocus()

        if event == 'e_phone1' and len(window[event].Get()) == 3:
            window['e_phone2'].SetFocus()
        if event == 'e_phone2' and len(window[event].Get()) == 3:
            window['e_phone3'].SetFocus()


    window.close()

    return values

def text_new_alumni_p5():
    frame_options = [[sg.Radio('Yes', 'options'),
                      sg.Radio('No', 'options')]]

    frame_education = [[sg.Radio('Yes', 'education'),
                        sg.Radio('No', 'education')]]

    frame_athletics = [[sg.Radio('Yes', 'athletics'),
                        sg.Radio('No', 'athletics')]]

    frame_arts = [[sg.Radio('Yes', 'arts'),
                    sg.Radio('No', 'arts')]]


    layout = [[sg.T('New Alumni - Page 5')],
              [sg.Frame('Options?', frame_options)],
              [sg.Frame('Education?', frame_education)],
              [sg.Frame('Athletics?', frame_athletics)],
              [sg.Frame('Performing Arts?', frame_arts)],
              [sg.Button('Finish', key='finish', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'finish':
            break

    window.close()

    return values

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