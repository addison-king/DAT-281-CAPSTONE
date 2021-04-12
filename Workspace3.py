# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:51:28 2021

@author: BKG
"""
from pathlib import Path
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid
import PySimpleGUI as sg

def main():

    print(ID_number)












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
    main()