# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:08:34 2021

@author: BKG
"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg
import re
from re import search
from datetime import datetime
from fpdf import FPDF

def main():

    alumni_number = lookup_alumni()
    alumni_basic = basic_info(alumni_number)
    alumni_contacts = contact_events(alumni_number)


    name = alumni_basic.at[0,'First Name'] + ' ' + alumni_basic.at[0,'Last Name']
    pdf = PDF(name)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    pdf.cell(0,15,'Basic Information', 0,1,'C')

    for i in alumni_basic.columns:
        pdf.cell(100, 8, i, 'LB', 0)
        pdf.cell(0, 8, alumni_basic.at[0,i], 'B', 1, 'R')

    pdf.add_page()

    pdf.cell(0,15,'All Contact Events', 0,1,'C')

    counter = 0
    for i in alumni_contacts.index:
        for j in alumni_contacts.columns:
            if j == 'Date of Contact':
                pdf.cell(50, 8, j, 'TLB', 0)
                pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 'TB', 'R')

            elif j == 'Notes':
                if len(alumni_contacts.at[i,j]) > 75:
                    pdf.cell(50, 8, j, 'L', 0)
                    pdf.set_font('Arial','',10)
                    pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 0, 'L')
                    pdf.set_font('Arial', '', 12)
                else:
                    pdf.cell(50, 8, j, 'L', 0)
                    pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 0, 'R')
            else:
                pdf.cell(50, 8, j, 'LB', 0)
                pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 'B', 'R')

        pdf.ln(15)
        counter -=- 1

        if counter % 2 == 0 and counter < len(alumni_contacts.index):
            pdf.add_page()
            pdf.cell(0,15,'All Contact Events', 0,1,'C')


    file_name = name + '.pdf'
    location = select_folder()
    write = location + '/' + file_name
    pdf.output(write, 'F')

class PDF(FPDF):
    def __init__(self, name):
        super(PDF, self).__init__()
        self.name = name

    def header(self):
        self.image('UIF-Logo.png', x=10, y=0, h=30)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, self.name, 'B', 0, 'C')
        self.ln(15)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def basic_info(alumni_number):

    query = '''SELECT *
               FROM Basic_Info
               WHERE ID_number = :id
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'id':alumni_number})
    connection.close()
    results = format_basic_info(results)

    return results


def format_basic_info(df):
    df = df.applymap(str)

    cols = df.columns.tolist()
    cols = [i.title() for i in df]

    for index, item in enumerate(cols):
        cols[index] = item.replace('_', ' ')

    df.columns = cols
    df.rename(columns = {'Id Number': 'ID Number',
                         'Health Info': 'Special Health Concerns',
                         'Phone Num': 'Phone Number',
                         'Address': 'Street Address',
                         'Parent Guardian': 'Parent | Guardian',
                         'Parent Guardian Phone Num': 'P|G Phone Number',
                         'Parent Guardian Email': 'P|G Email'},
                  inplace = True)

    df = df[['First Name','Last Name','ID Number','Core Student',
             'Graduation Year','Phone Number','Email','Birthday','Gender',
             'Street Address','City','State','Zipcode','Church','Highschool',
             'College','Job','Special Health Concerns','Parent | Guardian',
             'P|G Phone Number','P|G Email','Emergency Contact',
             'Emergency Contact Phone Number','Options','Education',
             'Athletics','Performing Arts']]

    # for i in df.columns:
    #     print(i, ' - ', df.at[0,i])

    return df


def contact_events(alumni_number):
    query = '''SELECT *
               FROM Contact_Events
               WHERE ID_number = :id
               ORDER BY contact_date desc
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'id':alumni_number})
    connection.close()

    results = format_contact_events(results)
    return results


def format_contact_events(df):
    df = df.applymap(str)
    df = df[['contact_date','spoke','track','status','notes']]
    df.rename(columns = {'contact_date': 'Date of Contact',
                         'spoke': 'Spoke to?',
                         'track': 'Current track',
                         'status': 'Track status',
                         'notes': 'Notes'},
                  inplace = True)

    # for j in df.index:
    #     for i in df.columns:
    #         print(i, ' - ', df.at[j,i])
    #     print('\n\n')
    return df





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

    window = sg.Window('UIF: Alumni Database', layout, size=(375,225))
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
    result = result['ID_number']

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


def select_folder():
    layout = [[sg.Text('Select a folder where the file will be saved:')],
              [sg.Input(), sg.FolderBrowse()],
              [sg.OK(), sg.Cancel()] ]

    window = sg.Window('UIF: Alumni Database', layout)
    values = window.read()
    window.close()
    if values[1][0] != '':
        return values[1][0]
    return None


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