# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12, 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

import PySimpleGUI as sg
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd

def main(location):
    perc_working = percentage_working()

    file_name = 'Percentage_Working.csv'
    os.chdir(location)
    perc_working.to_csv(file_name, index=False, encoding='utf-8')


def percentage_working():
    query = '''SELECT Last_Contact.ID_number, currently_employed, graduation_year
                FROM Last_Contact
                INNER JOIN Basic_Info on Basic_Info.ID_number = Last_Contact.ID_number
                ORDER BY graduation_year asc, currently_employed'''
    connection = _db_connection()
    data = pd.read_sql(query, con=connection)
    connection.close()
    result = pd.DataFrame(columns=['Graduation Year', 'Not Working', 'Working',
                                   'Total', 'Percentage Working'])

    for i in data.graduation_year.unique():
        raw_data = data.loc[data['graduation_year'] == i].value_counts(subset='currently_employed')

        if 'Yes' in raw_data.keys():
            yes = raw_data['Yes']
        else:
            yes = 0

        if 'No' in raw_data.keys():
            no = raw_data['No']
        else:
            no = 0

        total = no + yes
        perc_yes = round(yes/total, 3)
        # print('Graduation Year: ', i, '\nNot working: ', no, '\nWorking: ', yes,
        #       '\nTotal: ', total, '\nPercentage working: ', perc_yes, '%',
        #       '\n\n', sep='')
        dat = [i, no, yes, total, perc_yes]
        result.loc[len(result.index)] = dat

    # for i in result.index:
    #     print('Graduation Year:', int(result.at[i,'Graduation Year']))
    #     print('Percentage Working: ', round(result.at[i,'Percentage Working'], 1),'%' ,sep='')
    #     print()
    return result


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
    # location = 'C:\\Users\\falconfoe\\Desktop\\Testing'
    # main(location)
    main()
