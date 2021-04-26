# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 09:17:48 2021

@author: BKG
"""

import PySimpleGUI as sg
import re

sg.ChangeLookAndFeel('LightGreen')

layout = [[sg.Text('Time Input Validation Demonstration', font='Any 18')],
          [
           sg.In(key='_TIME1_', size=(4,1), change_submits=True, do_not_clear=True ), sg.T(':', pad=(0,0)),
           sg.In(key='_TIME2_', size=(4,1), change_submits=True, do_not_clear=True), sg.T(':', pad=(0,0)),
           sg.In(key='_TIME3_', size=(4,1), change_submits=True, do_not_clear=True)],
          [sg.Multiline(key='_M_', do_not_clear=True)],
          [sg.OK()]]

window = sg.Window('Demo - Input Validation', font=('Helvetica 14')).Layout(layout)

while True:
    event, values = window.Read()
    if event in (None, 'Quit', 'OK'):
        break
    if event in ('_TIME1_', '_TIME2_', '_TIME3_'):
        window.FindElement(event).Update(re.sub("[^0-9]", "", values[event]))
    if event == '_TIME1_' and len(window.FindElement(event).Get()) == 2:
        window.FindElement('_TIME2_').SetFocus()
    if event == '_TIME2_' and len(window.FindElement(event).Get()) == 2:
        window.FindElement('_TIME3_').SetFocus()
    if event == '_TIME3_' and len(window.FindElement(event).Get()) == 2:
        window.FindElement('_M_').SetFocus()
window.Close()