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
from re import search
from datetime import datetime

def main():
    values = page2()
    clean_val = clean_page2(values) #dict, {'Track':'', 'Status':'', 'Notes':''}


def clean_page2(values):
    temp = dict()
    for (key, value) in values.items():
        if value == True:
            if key == 'track_other':
                temp['track_other_input'] = values['track_other_input']
            elif key == 'status_other':
                temp['status_other_input'] = values['status_other_input']
            else:
                temp[key] = value

    clean = dict()
    track = ['college', 'military', 'ministry', 'trade', 'working', 'track_other']
    for i in track:
        for key in temp:
            if search(i, key):
                if i == 'track_other':
                    new = temp['track_other_input']
                    # print(new)
                    clean['Track'] = temp['track_other_input'].title()
                else:
                    new = key.replace('track_','').title()
                    clean['Track'] = new

    status = ['on_track', 'behind', 'graduated', 'full_time', 'part_time', 'unemployed', 'status_other']
    for i in status:
        for key in temp:
            if search(i, key):
                if i == 'status_other':
                    new = temp['status_other_input']
                    clean['Status'] = temp['status_other_input'].title()
                else:
                    new = key.replace('status_','').title()
                    clean['Status'] = new
    clean['Notes'] = values['notes'].strip('\n').title()

    return clean




def page2():
    frame_track = [[sg.Radio('College', 'track', key='track_college', enable_events=True),
                    sg.Radio('Military', 'track', key='track_military', enable_events=True),
                    sg.Radio('Ministry', 'track', key='track_ministry', enable_events=True)],
                   [sg.Radio('Trade School', 'track', key='track_trade', enable_events=True),
                    sg.Radio('Workforce', 'track', key='track_working', enable_events=True)],
                   [sg.Radio('Other', 'track', key='track_other', enable_events=True),
                    sg.In(key='track_other_input')]]



    frame_status = [[sg.Radio('On Track', 'status', key='status_on_track', enable_events=True),
                      sg.Radio('Behind', 'status', key='status_behind', enable_events=True),
                      sg.Radio('Graduated', 'status', key='status_graduated', enable_events=True)],
                    [sg.Radio('Full Time', 'status', key='status_full_time', enable_events=True),
                      sg.Radio('Part Time', 'status', key='status_part_time', enable_events=True),
                      sg.Radio('Unemployed', 'status', key='status_unemployed', enable_events=True)],
                    [sg.Radio('Other', 'status', key='status_other', enable_events=True),
                      sg.In(key='status_other_input')]]

    frame_notes = [[sg.Multiline(key='notes', size=(53,4))]]

    layout = [[sg.Frame('Post-Secondary Activity', frame_track)],
              [sg.Frame('Activity Status', frame_status)],
              [sg.Frame('Notes', frame_notes)],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            window.close()
            break

        elif event == 'track_other':
            window['track_other_input'].SetFocus()

        elif event == 'status_other':
            window['status_other_input'].SetFocus()

        elif event == 'OK':
            if sum([values['track_college'], values['track_military'],
                    values['track_ministry'], values['track_trade'],
                    values['track_working'], values['track_other']]) == 0:
                sg.popup_ok('Please select a Post-Secondary Activity option.')
            elif values['track_other'] == True and len(values['track_other_input']) == 0:
                sg.popup_ok('Please fill in the Post-Secondary Activity\n\"Other\" text field.')
            elif sum([values['status_on_track'], values['status_behind'],
                      values['status_graduated'], values['status_full_time'],
                      values['status_part_time'], values['status_unemployed'],
                      values['status_other']]) == 0:
                sg.popup_ok('Please select a Activity Status option.')
            elif values['status_other'] == True and len(values['status_other_input']) == 0:
                sg.popup_ok('Please fill in the Activity Status\n\"Other\" text field.')
            else:
                break

    window.close()
    return values




if __name__ == "__main__":

    main()