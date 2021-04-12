"""
Created on Mon Apr 12 09:17:14 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

# from pathlib import Path
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg

def main():
    """
    The main menu
    Present ths user with a gui and 4 buttons to choose from
    Based on what the user clicks on, executes other functions or closes

    Returns
    -------
    None.

    """
    _create_db_table()
    sg.theme('DarkBlue3')

    layout = [[sg.Text('Please select an action that you would like to perform:',
                       size=(25,3),
                       font=('Arial', 15))],
          [sg.Button('Import new alumni to the database',
                     key='alum',
                     size=(30,1))],
          [sg.Button('Import new interaction with alumni',
                     key='interaction',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Export list of alumni with ID numbers',
                     key='export_ID',
                     size=(30,1))],
          [sg.Button('Export list of next alumni to contact',
                     key='contact',
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
            _new_alumni_gui()
        elif event[0] == 'interaction':
            window.close()
            _new_interaction_gui()
        elif event[0] == 'export_ID':
            window.close()
            _export_alumni_name_list()
        elif event[0] == 'contact':
            window.close()
            #Call a fucntion to output the next call list
        elif event[0] in ('close', sg.WIN_CLOSED):
            break

    window.close()

def _select_file():
    layout = [[sg.Text('Folder Location')],
              [sg.Input(), sg.FileBrowse()],
              [sg.OK(), sg.Cancel()] ]

    window = sg.Window('UIF: Alumni Database', layout)
    values = window.read()
    window.close()
    return values[1][0]

def _select_folder():
    layout = [[sg.Text('Folder Location')],
              [sg.Input(), sg.FolderBrowse()],
              [sg.OK(), sg.Cancel()] ]

    window = sg.Window('UIF: Alumni Database', layout)
    values = window.read()
    window.close()
    return values[1][0]

def _all_good():
    layout = [[sg.Text('Everything completed without errors.',
               font=('Arial', 15))],
              [sg.Button('Exit the program', key='close')]]
    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event = window.read()
        if event[0] in ('close', sg.WIN_CLOSED):
            break
    window.close()

def _export_alumni_name_list():
    """
    Opens a connection to the database.
    Queries the database.
    Output is put into a dataframe.
    Dataframe is written to .csv file.

    Returns
    -------
    None.

    """
    connection = _db_connection()

    query = ''' SELECT alumni_ID, first_name, last_name,
                       graduation_year, CORE_student
                FROM Basic_Info
                ORDER BY last_name ASC
              '''

    output = pd.read_sql(query, con=connection)
    connection.close()
    col_names = ['ID Number',
                 'First Name',
                 'Last Name',
                 'Graduation Year',
                 'CORE?']
    output.columns = col_names
    file_name = 'Master Alumni List.csv'
    path = _select_folder()
    os.chdir(path)
    output.to_csv(file_name, index=False, encoding='utf-8')
    _all_good()

def _new_alumni_gui():
    location = _select_file()
    alumni_display = pd.read_csv(location)
    display_cols = ['Last Name',
                 'First Name',
                 'Graduation Year']
    alumni_display = alumni_display[display_cols]
    data = alumni_display.values.tolist()
    header_list = alumni_display.columns.tolist()

    layout = [[sg.Text('The following alumni will be added to the database:\n')],
              [sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))],
              [sg.Button('Confirm', key='import')],
              [sg.Button('Cancel', key='cancel')],
              [sg.Button('Main Menu', key='main')]]
    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event = window.read()
        if event[0] == 'import':
            window.close()
            _import_alumni(location)
            _all_good()
        elif event[0] == 'main':
            window.close()
            main()
        elif event[0] == 'cancel':
            window.close()
            main()
        elif event[0] == sg.WIN_CLOSED:
            break
    window.close()


def _new_interaction_gui():
    location = _select_file()
    interaction = pd.read_csv(location)
    display_cols = ['last_name',
                    'first_name',
                    'contact_date',
                    'notes']
    interaction = interaction[display_cols]
    data = interaction.values.tolist()
    header_list = interaction.columns.tolist()

    layout = [[sg.Text('The following alumni interactions will be added'+
                       'to the database: \n')],
              [sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))],
              [sg.Button('Confirm', key='import')],
              [sg.Button('Cancel - Do NOT Add', key='cancel')],
              [sg.Button('Main Menu', key='main')]]
    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event = window.read()
        if event[0] == 'import':
            _import_new_interaction(location)
        elif event[0] == 'main':
            window.close()
            main()
        elif event[0] in ('cancel', sg.WIN_CLOSED):
            break
    window.close()
    _all_good()

def _import_new_interaction(location):
    new_call = pd.read_csv(location)
    print(new_call)
    input(1)
    new_call['contact_date'] = pd.to_datetime(new_call['contact_date']).dt.strftime('%Y-%m-%d')
    connection = _db_connection()
    new_call.to_sql('Contact_Events', connection, index=False,
                    if_exists='append')
    connection.close()

def _import_alumni(location):
    """
    Reads in .csv with new alumni data.
    Drops the Timestamp col (generated from google forms).
    Renames the columns to match the database.
    Changes the case to titlecase for these cols: address, city, state,
                       church, highschool, college, job
    Checks to make sure the alumni doesn't already exist.
    Adds all new alumni to database where an ID number is assigned.
    Retrieves the new ID number, adds it to the dataframe.
    Then the dataframe containing all pertinent info is added to the database.

    Returns
    -------
    None.

    """

    alumni = pd.read_csv(location)
    alumni.drop('Timestamp', axis=1, inplace=True)
    col_names = ["last_name",
                "first_name",
                "CORE_student",
                "graduation_year",
                "phone_num",
                "birthday",
                "gender",
                "address",
                "city",
                "state",
                "zipcode",
                "email",
                "church",
                "highschool",
                "college",
                "job",
                "health_info",
                "parent_guardian",
                "parent_guardian_phone_num",
                "parent_guardian_email",
                "emergency_contact",
                "emergency_contact_phone_number",
                "OPTIONS",
                "education",
                "athletics",
                "performing_arts"]
    alumni.columns = col_names
    title_case_list = ['address',
                       'city',
                       'state',
                       'church',
                       'highschool',
                       'college',
                       'job']
    for i in title_case_list:
        alumni[i] = alumni[i].str.title()

    alumni['birthday'] = pd.to_datetime(alumni['birthday']).dt.strftime('%Y-%m-%d')

    query_1 = ''' SELECT COUNT(*), first_name, last_name, birthday
                FROM Alumni_ID
                WHERE last_name= :last AND first_name= :first AND birthday= :bday
                GROUP BY last_name
                '''
    connection = _db_connection()
    for i in alumni.index:
        last_name = alumni.loc[i,'last_name']
        first_name = alumni.loc[i,'first_name']
        bday = alumni.loc[i,'birthday']
        sq_df = pd.read_sql(query_1, params={'last': last_name,
                                        'first': first_name,
                                        'bday': bday},
                         con=connection)
        if len(sq_df) == 0:
            data = [[last_name, first_name, bday]]
            add_alumni = pd.DataFrame(data, columns = ['last_name',
                                                       'first_name',
                                                       'birthday'])
            add_alumni.to_sql('Alumni_ID', connection, index=False,
                      if_exists='append')
        else:
            print('\'',first_name,' ', last_name, '\' already exists..',
                  sep='')
    connection.commit()
    connection.close()

#import alumni now that IDs have been assigned
    query_2 = ''' SELECT alumni_ID
                  FROM Alumni_ID
                  WHERE first_name= :first AND
                        last_name= :last AND
                        birthday= :bday
                        '''
    connection = _db_connection()
    for i in alumni.index:
        last_name = alumni.loc[i, 'last_name']
        first_name = alumni.loc[i, 'first_name']
        bday = alumni.loc[i, 'birthday']

        sq_df = pd.read_sql(query_2, params={'last': last_name,
                                        'first': first_name,
                                        'bday': bday},
                         con=connection)
        if len(sq_df) == 1:
            alum_num = int(sq_df.loc[0,'alumni_ID'])
            alumni.at[i, 'alumni_ID'] = alum_num
            values = alumni.loc[i]
            new = pd.DataFrame(columns = alumni.columns)
            new = new.append(values, ignore_index = True)
            new.to_sql('Basic_Info', connection, index=False,
                          if_exists='append')
        else:
            print('DF error. length of:', len(sq_df))

    connection.commit()
    connection.close()

def _create_db_table():
    sql_table_basic = '''CREATE table IF NOT EXISTS Basic_Info (
                        alumni_ID integer,
                        last_name text,
                        first_name text,
                        CORE_student text,
                        graduation_year integer,
                        phone_num text,
                        birthday text,
                        gender text,
                        address text,
                        city text,
                        state text,
                        zipcode integer,
                        email text,
                        church text,
                        highschool text,
                        college text,
                        job text,
                        health_info text,
                        parent_guardian text,
                        parent_guardian_phone_num text,
                        parent_guardian_email text,
                        emergency_contact text,
                        emergency_contact_phone_number text,
                        OPTIONS text,
                        education text,
                        athletics text,
                        performing_arts text
                        )'''
    sql_table_contact = '''CREATE table IF NOT EXISTS Contact_Events (
                        alumni_ID integer,
                        last_name text,
                        first_name text,
                        contact_date text,
                        status text,
                        need text,
                        notes text
                        )'''
    sql_table_id = '''CREATE table IF NOT EXISTS Alumni_ID (
                        alumni_ID integer PRIMARY KEY AUTOINCREMENT,
                        last_name text,
                        first_name text,
                        birthday text
                        )'''
    sql_i_row = ''' INSERT INTO Alumni_ID (alumni_ID, last_name)
                    VALUES (1000, 'Test')
                    '''
    sql_delete_i_row = '''  DELETE FROM Alumni_ID
                            WHERE alumni_ID IS 1000 AND last_name IS 'Test'
                            '''

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(sql_table_basic)
    cursor.execute(sql_table_contact)
    cursor.execute(sql_table_id)
    cursor.execute(sql_i_row)
    cursor.execute(sql_delete_i_row)
    connection.commit()
    connection.close()

def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection

    '''
    try:
        connection = sqlite3.connect('MOCK_Data\\MOCK_Data.db')
    except Error:
        print(Error)
    return connection

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    main()
