"""
Created on Mon Apr 12 09:17:14 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

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
    os.chdir(os.path.dirname(sys.argv[0]))

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
            main_alum()

        elif event[0] == 'interaction':
            window.close()
            main_interaction()

        elif event[0] == 'export_ID':
            window.close()
            main_export_id()

        elif event[0] == 'contact':
            window.close()
            main_contact()

        elif event[0] in ('close', sg.WIN_CLOSED):
            break

    window.close()


def main_alum():
    location = select_file()
    if location is not None:
        new_alumni_gui(location)
    else:
        main()


def main_interaction():
    location = select_file()
    if location is not None:
        new_interaction_gui(location)
    else:
        main()


def main_export_id():
    location = select_folder()
    if location is not None:
        export_alumni_name_list(location)
    else:
        main()


def main_contact():
    location = select_folder()
    if location is not None:
        export_alumni_contact_list(location)
    else:
        main()


def select_file():
    layout = [[sg.Text('Folder Location')],
              [sg.Input(), sg.FileBrowse()],
              [sg.OK(), sg.Cancel()] ]

    window = sg.Window('UIF: Alumni Database', layout)
    values = window.read()
    window.close()
    if values[1][0] != '':
        return values[1][0]
    return None


def select_folder():
    layout = [[sg.Text('Folder Location')],
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
              [sg.Button('Exit the program', key='close')]]
    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event = window.read()
        if event[0] in ('close', sg.WIN_CLOSED):
            break
    window.close()


def export_alumni_name_list(path):
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

    query = ''' SELECT ID_number, first_name, last_name,
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
    # path = select_folder()
    os.chdir(path)
    output.to_csv(file_name, index=False, encoding='utf-8')
    all_good()


def export_alumni_contact_list(path):
    query_read = '''SELECT c.ID_number, c.first_name, c.last_name,
                           c.CORE_student, c.last_date, b.phone_num, b.email
                    FROM Last_Contact c
                    INNER JOIN Basic_Info b
                        ON c.ID_number = b.ID_number
                    WHERE last_date < DATE('now', '-90 days')
                    ORDER BY c.CORE_student DESC, c.last_date ASC
                 '''

    connection = _db_connection()
    contact = pd.read_sql(query_read, con=connection)
    connection.close()
    col_names = ['ID Number',
                 'First Name',
                 'Last Name',
                 'CORE?',
                 'Last Contact Date',
                 'Phone Number',
                 'Email']
    contact.columns = col_names
    file_name = 'Alumni to Contact.csv'
    # path = select_folder()
    os.chdir(path)
    contact.to_csv(file_name, index=False, encoding='utf-8')
    all_good()


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
            import_alumni_p1(location)
            all_good()
        elif event[0] == 'main':
            window.close()
            main()
        elif event[0] == 'cancel':
            window.close()
            main()
        elif event[0] == sg.WIN_CLOSED:
            break
    window.close()


def new_interaction_gui(location):

    interaction = pd.read_csv(location)
    col_names = ['ID_number',
                 'first_name',
                 'last_name',
                 'contact_date',
                 'status',
                 'need',
                 'notes']
    interaction.columns = col_names
    display_cols = ['last_name',
                    'first_name',
                    'contact_date',
                    'notes']
    interaction['contact_date'] = pd.to_datetime(interaction['contact_date']).dt.strftime('%Y-%m-%d')
    display = interaction[display_cols]
    data = display.values.tolist()
    header_list = display.columns.tolist()

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
            window.close()
            import_new_interaction(interaction)
            update_last_contact(interaction)
        elif event[0] == 'main':
            window.close()
            main()
        elif event[0] in ('cancel', sg.WIN_CLOSED):
            break
    window.close()
    all_good()


def update_last_contact(interaction):
    query_read = '''SELECT ID_number, last_date
                 FROM Last_Contact
                 WHERE ID_number = :id
              '''
    query_write = '''UPDATE Last_Contact
                 SET last_date = ?
                 WHERE ID_number = ?
              '''
    connection = _db_connection()
    cursor = connection.cursor()
    for i in interaction.index:
        id_num = int(interaction.loc[i, 'ID_number'])
        date_df = pd.read_sql(query_read,
                              con=connection,
                              params={'id':id_num})
        if date_df.iloc[0]['last_date'] < interaction.iloc[i]['contact_date']:
            cursor.execute(query_write,
                           (interaction.iloc[i]['contact_date'], id_num))
            connection.commit()
        else:
            print(interaction.iloc[i]['contact_date'], 'is too old..')
    connection.close()


def import_new_interaction(interaction):

    interaction['contact_date'] = pd.to_datetime(interaction['contact_date']).dt.strftime('%Y-%m-%d')
    connection = _db_connection()
    interaction.to_sql('Contact_Events', connection, index=False,
                    if_exists='append')
    connection.close()


def import_alumni_p1(location):

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
    alumni = alumni.fillna('None')
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
                new.to_sql('Basic_Info', connection, index=False,
                              if_exists='append')
            else:
                print('DF error. length of:', len(sq_df))

        connection.commit()
        connection.close()
        import_alumni_p3()
    else:
        print('Nothing to add.')

def import_alumni_p3():

#initialize all the new alumni to the "Last_Contact" Table
    connection = _db_connection()
    query = ''' SELECT ID_number, first_name, last_name,
                       CORE_student, graduation_year
                FROM Basic_Info
                ORDER BY last_name ASC
              '''
    output = pd.read_sql(query, con=connection)
    connection.close()
    col_names = ['ID_number',
                 'first_name',
                 'last_name',
                 'CORE_student',
                 'graduation_year']
    output.columns = col_names
    for i in output.index:
        last_date = str(output.iloc[i,4])
        last_date = last_date + '-06-01'
        output.at[i, 'last_date'] = last_date

    output['last_date'] = pd.to_datetime(output['last_date']).dt.strftime('%Y-%m-%d')
    output.drop(columns=['graduation_year'], inplace = True)
    output = output[['ID_number',
                     'last_name',
                     'first_name',
                     'CORE_student',
                     'last_date']]
    connection = _db_connection()
    output.to_sql('Last_Contact', connection, index=False,
                    if_exists='append')
    connection.close()

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
