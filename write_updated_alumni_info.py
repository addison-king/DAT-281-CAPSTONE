# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:08:34 2021

@author: BKG
"""

import sqlite3
from sqlite3 import Error


def main(alumni):

    alumni = alumni.applymap(str)

    query = '''UPDATE Basic_Info '''

    for i, value in enumerate(alumni):

        if value != 'ID_number':

            if i == 1:
                temp = '''SET ''' + value + ''' = \'''' + alumni.at[0, value] + '\', '

            elif i+1 == len(alumni.columns):
                temp = value + ''' = \'''' + alumni.at[0, value] + '\''

            else:
                temp = value + ''' = \'''' + alumni.at[0, value] + '\', '

            query = query + temp

    where = ''' WHERE ID_number = ''' + str(alumni.at[0,'ID_number'])
    temp_query = query + where

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(temp_query)
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
        connection = sqlite3.connect('Data\\UIF_Alumni_DB.db')
    except Error:
        print(Error)
    return connection


if __name__ == "__main__":
    # test_data = {'ID_number': 1001,
    #          'first_name': 'Addison',
    #          'last_name': 'Smith',
    #          'gender': 'Female'}
    # results = pd.DataFrame(test_data, index=[0])
    # main(results)
    main()