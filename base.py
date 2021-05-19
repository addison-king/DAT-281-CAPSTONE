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

import create_new_alumni #GUI where the user inputs information about an alum
import create_new_interaction #GUI where the user inputs a new alumni interaction
import alumni_to_db #writes a new alumni to the db
import interaction_to_db #writes a new alumni interaction to the db
import export_name_list #exports a .csv file with full list of names from db
import export_call_list #exports a .csv file with a list of alumni to contact next
import export_single_all_info #exports a .pdf file with all information on one alumni
import export_percentage_working #exports a .csv file, sep by grad year comparing working/not
import export_percentage_graduated #exports a .csv file, number of graduated alumni
import get_updated_alumni_info #prompts the user to input new changes to an alumni
import write_updated_alumni_info #all changes to an alumni are writte to the db
import advanced_query #gui window where you can query the DB
import advanced_csv_import #ability to import a csv of new alumni


def main():
    """
    The main menu
    Present ths user with a gui and 4 buttons to choose from
    Based on what the user clicks on, executes other functions or closes

    Returns
    -------
    None.

    """

    os.chdir(os.path.dirname(sys.argv[0]))

    sg.theme('DarkBlue3')

    layout = [[sg.Text('Please select an action that you would like to perform:',
                       size=(25,3),
                       font=('Arial', 15))],
          [sg.Button('Create a new alumni for the database',
                     key='alum',
                     size=(30,1))],
          [sg.Button('Create a new interaction with an alumni',
                     key='interaction',
                     size=(30,1))],
          [sg.Button('Update the information on an alumni',
                     key='update_basic',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Export list of alumni with ID numbers',
                     key='export_ID',
                     size=(30,1))],
          [sg.Button('Export list of next alumni to contact',
                     key='contact',
                     size=(30,1))],
          [sg.Button('Export percentage of alumni working\nper graduation class',
                     key='perc_work',
                     size=(30,2)),],
          [sg.Button('Export percentage of alumni that\n'+
                     'have graduated higher education',
                     key='perc_grad',
                     size=(30,2))],
          [sg.Button('Select an alumni and export all data',
                     key='export_all',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Advanced',
                     key='advanced',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Close the program',
                     key='close',
                     size=(30,1))]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event = window.read()

        if event[0] == 'alum':
            window.close()
            main_add_alum()

        elif event[0] == 'interaction':
            window.close()
            main_new_interaction()

        elif event[0] == 'update_basic':
            window.close()
            update_basic_info()

        elif event[0] == 'export_ID':
            window.close()
            main_export_id()

        elif event[0] == 'contact':
            window.close()
            main_export_contact()

        elif event[0] == 'perc_work':
            window.close()
            main_export_perc_work()

        elif event[0] == 'perc_grad':
            window.close()
            main_export_perc_grad()

        elif event[0] == 'export_all':
            window.close()
            export_single_all_info.main()
            # all_good()
            main()

        elif event[0] == 'advanced':
            window.close()
            main_advanced()
            main()

        elif event[0] in ('close', sg.WIN_CLOSED):
            break

    window.close()


def main_add_alum():
#GUI which the user enters new alum data.
    alumni_df = create_new_alumni.main()

#If the user selected 'Cancel' then it returns None and 'else' goes to main.
    if isinstance(alumni_df, pd.DataFrame):
        alumni_to_db.main(alumni_df)
        all_good()
        main()
    else:
        print('None value - main add alumni')
        main()


def main_new_interaction():
    interaction = create_new_interaction.main()

    if isinstance(interaction, pd.DataFrame):
        interaction_to_db.main(interaction)
        all_good()
        main()
    else:
        print('None value - main new interaction')
        main()

def update_basic_info():
    alumni_df = get_updated_alumni_info.main()
    if isinstance(alumni_df, pd.DataFrame):
        write_updated_alumni_info.main(alumni_df)
        all_good()
        main()
    else:
        print('None value - update basic info')
        main()

def main_export_id():
    location = select_folder()
    if location is not None:
        export_name_list.main(location) #.py file main function
        all_good()
        main()
    else:
        main()


def main_export_contact():
    location = select_folder()
    if location is not None:
        export_call_list.main(location) #.py file main function
        all_good()
        main()
    else:
        main()

def main_export_perc_work():
    location = select_folder()
    if location is not None:
        export_percentage_working.main(location) #.py file main function
        all_good()
        main()
    else:
        main()


def main_export_perc_grad():
    location = select_folder()
    if location is not None:
        export_percentage_graduated.main(location) #.py file main function
        all_good()
        main()
    else:
        main()


def main_advanced():
    layout = [[sg.Text('Please select an action that you would like to perform:',
                       size=(25,3),
                       font=('Arial', 15))],
          [sg.Button('Import new alumni from a .csv file',
                     key='csv',
                     size=(30,1))],
          [sg.Button('Query the databse',
                     key='query',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Return to Main Menu',
                     key='main',
                     size=(30,1))]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event = window.read()

        if event[0] == 'csv':
            window.close()
            advanced_csv_import.main()

        elif event[0] == 'query':
            window.close()
            advanced_query.main()


        elif event[0] in ('main', sg.WIN_CLOSED):
            break

    window.close()

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


def all_good():
    layout = [[sg.Text('Everything completed without errors.',
               font=('Arial', 15))],
              [sg.Button('Return to Main Menu', key='close')]]
    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event = window.read()
        if event[0] in ('close', sg.WIN_CLOSED):
            break
    window.close()


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
