# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:08:34 2021

@author: BKG
"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg
import re
from datetime import datetime


def main(list_test):
    frame_track = [[sg.Radio('College', 'track', key='track_college', enable_events=True),
                    sg.Radio('Working', 'track', key='track_working', enable_events=True)]]
    
    # frame_status = [[sg.Radio('Test', 'status', key='status_one', enable_events=True),
    #                  sg.Radio('', 'status', key='status_two', enable_events=True),
    #                  sg.Radio('', 'status', key='status_three', enable_events=True)]]
    
    frame_status = [[sg.Combo(list_test, key='status', size=(55,1))]]

    frame_notes = [[sg.Multiline(key='notes', size=(55,4))]]

    layout = [[sg.Frame('Post-Secondary Track', frame_track)],
              [sg.Frame('Alumni Status', frame_status)],
              [sg.Frame('Notes', frame_notes)],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('UIF: Alumni Database', layout, size=(500,500))

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
    
        elif event == 'track_college':
            print('Here')

            list_test = ['On Track', 'Behind', 'Graduated']
            window.close()
            main(list_test)
            
            
def college():
    frame_track = [[sg.T('College')]]
    


if __name__ == "__main__":
    list_test = ['test1','test2','test3','test4']
    main(list_test)