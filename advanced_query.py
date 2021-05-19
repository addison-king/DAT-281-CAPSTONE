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
import PySimpleGUI as sg


def main():
    """
    This GUI window allows the user to type in SQLite commands and view the
        results. For any future programmer, I wished to pretty print the
        output, but didn't have time.

    Returns
    -------
    None.

    """

    layout = [[sg.Text('Use this window to query the databse.')],
              [sg.Multiline(size=(100, 10), key='sql_input')],
              [sg.Text('_'  * 100, size=(100, 1))],
              [sg.Multiline(size=(100,10), enable_events=True,
                            do_not_clear=True, key='sql_output')],
              [sg.Button('Submit', key='query', size=(30,1)),
               sg.T('     '),
               sg.Button('Main Menu', key='main', size=(30,1))]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event == 'query':
            answer = query_db(values['sql_input'])
            window['sql_output'].Update(answer)

        if event in ('main', sg.WIN_CLOSED):
            break
    window.close()


def query_db(query):
    """
    Literally sends the users input to the db then returns the result.

    Parameters
    ----------
    query : STR
        Hopefully a command that makes sense to the db

    Returns
    -------
    rows : LIST
        List of the resulting values. Note, this is missing the col headers.

    """
    # print(query)
    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    # print(type(rows))

    return rows


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
