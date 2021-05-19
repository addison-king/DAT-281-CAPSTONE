# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12, 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg


def main(location):
    """
    Calculates the percentage of after high school activities graduates.
    Writes the resulting values to .csv

    Parameters
    ----------
    location : String
        Windows folder location the user selected.

    Returns
    -------
    None.

    """

    perc_data = percentage_graduated()

    file_name = 'Percentage_Graduated.csv'
    os.chdir(location)
    perc_data.to_csv(file_name, index=False, encoding='utf-8')


def percentage_graduated():
    query_grad = '''SELECT COUNT(*)
                    FROM Contact_Events
                    WHERE status = \'Graduated\''''

    query_contacted = '''SELECT COUNT(DISTINCT ID_number)
                         FROM Contact_Events'''

    query_tot = '''SELECT COUNT(*)
                    FROM Alumni_ID'''

    connection = _db_connection()
    grad = pd.read_sql(query_grad, con=connection)
    contact = pd.read_sql(query_contacted, con=connection)
    total = pd.read_sql(query_tot, con=connection)
    connection.close()

    graduated = grad.at[0,'COUNT(*)']
    contacted = contact.at[0, 'COUNT(DISTINCT ID_number)']
    total = total.at[0,'COUNT(*)']

    perc_grad_con = round(graduated/contacted,3)
    perc_grad_tot = round(graduated/total,3)

    data = {'Graduated': graduated,
            'Alumni Contacted': contacted,
            'Total Alumni': total,
            'Graduation Percentage of Contacted': perc_grad_con,
            'Graduation Percetage in Total': perc_grad_tot}
    result = pd.DataFrame(data, index=[0])

    return result


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
