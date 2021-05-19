# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12, 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

import datetime
import PySimpleGUI as sg
import sqlite3
from sqlite3 import Error
import pandas as pd


def main():
    """
    Allows the user to select a .csv file and import

    Returns
    -------
    None.

    """

    location = select_file()
    if location is not None:
        new_alumni_gui(location)


def new_alumni_gui(location):
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
            sg.popup_ok('This may take a few seconds.\n\nThere will be no window\n'+
                        'while the program works.\nPlease be patient.'+
                        '\nPress OK to begin importation.')
            import_alumni_p1(location)

        elif event[0] in  (sg.WIN_CLOSED, 'cancel', 'main'):
            window.close()
            break
    window.close()


def import_alumni_p1(location):

    alumni = pd.read_csv(location)

    col_names = ["last_name", "first_name", "CORE_student","graduation_year",
                "phone_num", "birthday", "gender", "address", "city", "state",
                "zipcode", "email", "church", "highschool", "college", "job",
                "health_info", "parent_guardian", "parent_guardian_phone_num",
                "parent_guardian_email", "emergency_contact",
                "emergency_contact_phone_number", "OPTIONS", "education",
                "athletics", "performing_arts"]

    alumni.columns = col_names
    title_case_list = ['address',
                       'city',
                       'state',
                       'church',
                       'highschool',
                       'college',
                       'job']
    alumni = alumni.fillna('None')
    for i in title_case_list:
        alumni[i] = alumni[i].str.title()

    for i in alumni.index:
        if alumni.at[i, 'birthday'] != 'None':
            temp = datetime.datetime.strptime(alumni.at[i, 'birthday'], '%m/%d/%Y')
            alumni.at[i, 'birthday'] = datetime.datetime.strftime(temp, '%Y-%m-%d')



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
            alumni = alumni.drop(i)
    connection.commit()
    connection.close()
    import_alumni_p2(alumni)


def import_alumni_p2(alumni):
#import alumni now that IDs have been assigned
    if len(alumni) != 0:
        query_2 = ''' SELECT ID_number
                      FROM Alumni_ID
                      WHERE first_name= :first AND
                            last_name= :last AND
                            birthday= :bday
                            '''
        connection = _db_connection()
        id_list = []
        for i in alumni.index:
            last_name = alumni.loc[i, 'last_name']
            first_name = alumni.loc[i, 'first_name']
            bday = alumni.loc[i, 'birthday']

            sq_df = pd.read_sql(query_2, params={'last': last_name,
                                            'first': first_name,
                                            'bday': bday},
                             con=connection)
            if len(sq_df) == 1:
                alum_num = int(sq_df.loc[0,'ID_number'])
                alumni.at[i, 'ID_number'] = alum_num
                values = alumni.loc[i]
                new = pd.DataFrame(columns = alumni.columns)
                new = new.append(values, ignore_index = True)
                new.drop(['last_name', 'first_name', 'birthday'], axis=1, inplace=True)
                new.to_sql('Basic_Info', connection, index=False,
                              if_exists='append')
                id_list.append(alum_num)
            else:
                print('DF error. length of:', len(sq_df))

        connection.commit()
        connection.close()

        id_df = pd.DataFrame({'ID_number': id_list})
        import_alumni_p3(id_df)
    else:
        print('Nothing to add.')

def import_alumni_p3(id_df):
#initialize all the new alumni to the "Last_Contact" Table

    query = '''SELECT ID_number, graduation_year, job
                FROM Basic_Info
                WHERE ID_number = :id'''

    for i in id_df.index:
        connection = _db_connection()

        id_num = int(id_df.at[i, 'ID_number'])

        output = pd.read_sql(query,
                              con=connection,
                              params={'id':id_num})
        connection.close()

        col_names = ['ID_number',
                     'graduation_year',
                     'occupation']
        output.columns = col_names

        if output.at[0, 'occupation'] != 'None':
            data = ['Yes']
            output['currently_employed'] = data
        else:
            data = ['No']
            output['currently_employed'] = data

        if output.at[0,'graduation_year'] == 'None':
            output.at[0,'graduation_year'] = 2010

        for i in output.index:
            last_date = str(output.at[i, 'graduation_year'])
            last_date = last_date + '-01-01'
            output.at[i, 'last_date'] = last_date

        output['last_date'] = pd.to_datetime(output['last_date']).dt.strftime('%Y-%m-%d')
        output.drop(columns=['graduation_year'], inplace = True)
        output = output[['ID_number',
                         'last_date',
                         'currently_employed',
                         'occupation']]

        connection = _db_connection()

        output.to_sql('Last_Contact', connection, index=False,
                        if_exists='append')
        connection.commit()
        connection.close()


def select_file():
    layout = [[sg.Text('File Location')],
              [sg.Input(), sg.FileBrowse()],
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
