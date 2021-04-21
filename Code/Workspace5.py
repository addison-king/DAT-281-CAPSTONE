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
    values_page_1 = text_new_alumni_p2()
    print(values_page_1)


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

    frame_gender = [[sg.Radio('Female', 'gender', key='gender_female'),
                     sg.Radio('Male', 'gender', key='gender_male')]]

    frame_street_ad = [[sg.In(key='street_address', size=(49,1))]]

    frame_city = [[sg.Radio('Pittsburgh', 'city', key='city_pgh', default=True),
                   sg.Radio('Other', 'city', key='city_other'),
                   sg.In(key='city_input', size=(25,1))]]

    frame_state = [[sg.Radio('Pennsylvania', 'state', key='state_pa', default=True),
                    sg.Radio('Other', 'state', key='state_other'),
                    sg.In(key='state_input', size=(23,1))]]

    frame_zipcode = [[sg.In(key='zipcode', size=(6,1),
                            change_submits=True, do_not_clear=True),
                      sg.T('', key='error_zipcode', text_color='purple', size=(36,2))]]

    frame_missing_val = [[sg.T('', key='main_error', text_color='white', size=(43,1))]]

    layout = [[sg.T('New Alumni - Page 2')],
              [sg.Frame('Birthday (mm-dd-yyyy)', frame_birthday)],
              [sg.Frame('Gender', frame_gender)],
              [sg.Frame('Street Address', frame_street_ad)],
              [sg.Frame('City', frame_city)],
              [sg.Frame('State', frame_state)],
              [sg.Frame('Zipcode', frame_zipcode)],
              [sg.Frame('Error Checking', frame_missing_val)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)
    

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            window.close()
            break
        if event == 'next_page':
            if sum([values['gender_male'], values['gender_female']]) == 0:
                    window['main_error'].Update('Please select a Gender')
                    window['main_error'].Widget.config(background='red')
            elif sum([values['gender_male'], values['gender_female']]) != 0:
                    window['main_error'].Update('')
                    window['main_error'].Widget.config(background='#64778D')
                    break
            
                
                
            
            
        if event in ('bday_month', 'bday_day', 'bday_year', 'zipcode'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'bday_month' and len(window[event].Get()) >= 1:
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

        if event == 'zipcode' and len(window[event].Get()) >= 1:
            if not re.match('^\d{5}$', window[event].Get()):
                window['error_zipcode'].Update('Please enter a 5 digit zipcode\n(e.g. 15212).')
                window['zipcode'].Widget.configure(highlightcolor='red', highlightthickness=2)
            else:
                window['error_zipcode'].Update('')
                window['zipcode'].Widget.configure(highlightcolor='white')


    window.close()

    return values




if __name__ == "__main__":
    main()