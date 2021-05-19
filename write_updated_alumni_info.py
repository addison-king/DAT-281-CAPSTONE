# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12, 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

import sqlite3
from sqlite3 import Error


def main(alumni):
    """


    Parameters
    ----------
    alumni : pd.DataFrame
        Contains all the values the user inputted from the GUI that need to be
            written to the db.

    Returns
    -------
    None.

    """

    alumni = alumni.applymap(str)
    if 'last_name' in alumni.columns:
        alumni = write_last_name(alumni)

    if 'first_name' in alumni.columns:
        alumni = write_first_name(alumni)

    if 'birthday' in alumni.columns:
        alumni = write_birthday(alumni)


    query = '''UPDATE Basic_Info '''
    for i, value in enumerate(alumni):

        if value != 'ID_number':

            if i == 1 and len(alumni.columns) > 1:
                temp = '''SET ''' + value + ''' = \'''' + alumni.at[0, value] + '\', '

            elif i+1 == len(alumni.columns):
                temp = value + ''' = \'''' + alumni.at[0, value] + '\''

            else:
                temp = value + ''' = \'''' + alumni.at[0, value] + '\', '

            query = query + temp

    where = ''' WHERE ID_number = ''' + str(alumni.at[0,'ID_number'])
    query = query + where

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()


def write_last_name(df):

    query = '''UPDATE Alumni_ID '''
    temp = '''SET last_name = \'''' + df.at[0, 'last_name'] + '\''
    where = ''' WHERE ID_number = ''' + str(df.at[0,'ID_number'])
    query = query + temp + where

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

    df.drop(['last_name'], axis=1, inplace=True)

    return df


def write_first_name(df):

    query = '''UPDATE Alumni_ID '''
    temp = '''SET first_name = \'''' + df.at[0, 'first_name'] + '\''
    where = ''' WHERE ID_number = ''' + str(df.at[0,'ID_number'])
    query = query + temp + where

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

    df.drop(['first_name'], axis=1, inplace=True)

    return df

def write_birthday(df):

    query = '''UPDATE Alumni_ID '''
    temp = '''SET birthday = \'''' + df.at[0, 'birthday'] + '\''
    where = ''' WHERE ID_number = ''' + str(df.at[0,'ID_number'])
    query = query + temp + where

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

    df.drop(['birthday'], axis=1, inplace=True)

    return df


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
    # test_data = {'ID_number': 1007,
    #           'first_name': 'Addison2',
    #           'last_name': 'Smithson',
    #           'gender': 'Female',
    #           'city':'Some city',
    #           'state':'New York',
    #           'zipcode':15212}
    # results = pd.DataFrame(test_data, index=[0])
    # main(results)
    main()
