# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 08:45:45 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""
import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg
import re
from datetime import datetime


def main():

    alumni = None
    values_p1 = None
    values_p2 = None
    values_p2_truth = None

    alumni = lookup_alumni() #DICTIONARY
    alumni.pop('birthday', None)
    # print(alumni)

    if alumni != None:
        values_p1 = interaction_p1() #DICTIONARY

    if values_p1 != None:
        if values_p1['spoke_no'] == True:
            values_p2 = {'notes': 'None', 'status': 'None', 'need': 'None'}
            values_p2_truth = False
        else:
            values_p2 = interaction_p2() #DICTIONARY
            values_p2_truth = True
            
    if not None in [alumni, values_p1, values_p2]:
        if values_p2_truth == True:
            values_p1 = clean_page_1(values_p1)
            values_p2 = clean_page_2(values_p2)
        else:
            values_p1 = clean_page_1(values_p1)
        
        dicts = merge_dicts(alumni, values_p1, values_p2)
        result = pd.DataFrame([dicts], columns=dicts.keys())
        
        result = format_df(result)
        
    else:
        print('None value. Quit.')
        result = None
    
    return result

def format_df(df):
    df = df[['ID_number','last_name', 'first_name', 'contact_date', 
             'spoke', 'status', 'need', 'notes']]
    df = df.fillna('None')
    df['contact_date'] = pd.to_datetime(df['contact_date']).dt.strftime('%Y-%m-%d')
    
    return df

def merge_dicts(al, p1, p2):
    al.update(p1)
    al.update(p2)
    return al


def clean_page_1(values):

#Format the datetime value to be yyyy-mm-dd
    temp_date = values['date']
    temp_date = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    values['contact_date'] = temp_date

    values.pop('date', None)
    values.pop('Choose Date', None)

    if values['spoke_yes'] == True:
        values['spoke'] = 'Yes'
        values.pop('spoke_yes', None)
        values.pop('spoke_no', None)
    elif values['spoke_no'] == True:
        values['spoke'] = 'No'
        values.pop('spoke_yes', None)
        values.pop('spoke_no', None)


    return values #dict {'date':'yyyy-mm-dd', 'spoke':'Yes | No'}


def clean_page_2(values):

    if values['status_good'] == True:
        values['status'] = 'Good'
        values.pop('status_good', None)
        values.pop('status_poor', None)
        values.pop('status_other', None)
        values.pop('status_input', None)
    elif values['status_poor'] == True:
        values['status'] = 'Poor'
        values.pop('status_good', None)
        values.pop('status_poor', None)
        values.pop('status_other', None)
        values.pop('status_input', None)
    elif values['status_other'] == True:
        values['status'] = values['status_input']
        values.pop('status_good', None)
        values.pop('status_poor', None)
        values.pop('status_other', None)
        values.pop('status_input', None)

    if values['need_yes'] == True:
        values['need'] = 'Yes'
        values.pop('need_yes', None)
        values.pop('need_no', None)
    elif values['need_no'] == True:
        values['need'] = 'No'
        values.pop('need_yes', None)
        values.pop('need_no', None)


    return values #dict {'notes':'STRING', 'status':'STRING', 'need':'Yes | No'}


def lookup_alumni():

    frame_id_number = [[sg.Input(key='id_num',
                                 change_submits=True, do_not_clear=True)]]

    frame_first_name = [[sg.Input(key='first')]]

    frame_last_name = [[sg.Input(key='last')]]

    layout = [
        [sg.Frame('Alumni ID Number', frame_id_number)],
        [sg.T('OR')],
        [sg.Frame('First Name', frame_first_name)],
        [sg.Frame('Last Name', frame_last_name)],
        [sg.Button('Lookup Alumni', key='lookup', size=(15,1)), sg.Cancel()]
        ]

    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            result = None
            break

        elif event in ('id_num'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        elif event == 'lookup':
            if len(values['id_num']) != 0:
                result = sql_lookup_num(values['id_num'])

                if not isinstance(result, pd.DataFrame):
                    sg.popup_ok('Could not find an alumni.\nPlease try again.')

                else:
                    first = str(result.iloc[0]['first_name'])
                    last = str(result.iloc[0]['last_name'])
                    grad_yr = str(result.iloc[0]['graduation_year'])
                    bday = str(result.iloc[0]['birthday'])
                    str_out = ('Found the following alumni: \n\nName: ' + first
                               + ' ' + last + '\nGraduation Year: ' + grad_yr +
                               '\nBirthday: ' + bday +
                                '\n\nIs this correct?')
                    if sg.popup_yes_no(str_out) == 'Yes':
                        
                        temp = result.to_dict('records')
                        result = temp[0]
                        break

            elif sum([len(values['first']), len(values['last'])]) >= 2:
                result = sql_lookup_name(values['first'], values['last'])

                if not isinstance(result, pd.DataFrame):
                    sg.popup_ok('Could not find an alumni.\nPlease try again.')

                else:
                    first = str(result.iloc[0]['first_name'])
                    last = str(result.iloc[0]['last_name'])
                    grad_yr = str(result.iloc[0]['graduation_year'])
                    bday = str(result.iloc[0]['birthday'])
                    str_out = ('Found the following alumni: \n\nName: ' + first
                               + ' ' + last + '\nGraduation Year: ' + grad_yr +
                               '\nBirthday: ' + bday +
                                '\n\nIs this correct?')
                    if sg.popup_yes_no(str_out) == 'Yes':
                        
                        temp = result.to_dict('records')
                        result = temp[0]
                        break

    window.close()
    
    return result


def sql_lookup_name(first, last):

    query = '''SELECT first_name, last_name, graduation_year, birthday, ID_number
               FROM Basic_Info
               WHERE first_name = :first and last_name = :last
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'first':first, 'last':last})
    connection.close()

    if len(results) == 0:
        results = None

    return results


def sql_lookup_num(id_num):

    query = '''SELECT first_name, last_name, graduation_year, birthday, ID_number
               FROM Basic_Info
               WHERE ID_number = :id
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'id':id_num})
    connection.close()

    if len(results) == 0:
        results = None

    return results


def interaction_p1():
    frame_date = [[sg.In(key='date'), sg.CalendarButton('Choose Date')]]

    frame_spoke_to = [[sg.Radio('Yes', 'spoke', key='spoke_yes', enable_events=True),
                       sg.Radio('No', 'spoke', key='spoke_no', enable_events=True)]]

    layout = [[sg.Frame('Date of Contact', frame_date)],
              [sg.Frame('Did you speak to the alumni?', frame_spoke_to)],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break

        elif event == 'OK':
            if len(values['date']) == 0:
                sg.popup_ok('Please select a date which\n' +
                            'you contacted the alumni.')

            elif sum([values['spoke_yes'], values['spoke_no']]) == 0:
                sg.popup_ok('Please select an option if you\n' +
                            'spoke to the alumni or not.')

            elif (len(values['date']) != 0 and
                  sum([values['spoke_yes'], values['spoke_no']]) == 1):
                break
            

    window.close()
    return values


def interaction_p2():

    frame_status = [[sg.Radio('Good', 'status', key='status_good', enable_events=True),
                     sg.Radio('Poor', 'status', key='status_poor', enable_events=True)],
                     [sg.Radio('Other', 'status', key='status_other', enable_events=True),
                      sg.In(key='status_input')]]

    frame_need = [[sg.Radio('Yes', 'need', key='need_yes', enable_events=True),
                   sg.Radio('No', 'need', key='need_no', enable_events=True)]]

    frame_notes = [[sg.Multiline(key='notes', size=(55,4))]]

    layout = [[sg.Frame('Alumni Status', frame_status)],
              [sg.Frame('Is the Alumni requesting a need to be met?',
                        frame_need)],
              [sg.Frame('Notes', frame_notes)],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break

        elif event == 'OK':
            if sum([values['status_good'],
                    values['status_poor'],
                    values['status_other']]) == 0:
                sg.popup_ok('Please select an option that best\n' +
                            'describes the Alumni Status.')
            elif values['status_other'] == True and len(values['status_input']) == 0:
                sg.popup_ok('\"Other\" status selected. Please fill\n' +
                            'in the box describing the status.')
            elif sum([values['need_yes'], values['need_no']]) == 0:
                sg.popup_ok('Please select if the alumni asked\n' +
                            'for a need to be met.')
            elif sum([values['status_good'],
                      values['status_poor'],
                      values['status_other'],
                      values['need_yes'],
                      values['need_no']]) == 2:
                break


        elif event in ('need_yes', 'need_no'):
            window['notes'].SetFocus()

        elif event == 'status_other':
            window['status_input'].SetFocus()

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