# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 10:22:52 2021

@author: BKG
"""

import PySimpleGUI as sg

layout = [
            [sg.Text('My layout', key='_TEXT_')],
            [sg.Input(key='_INPUT_')],
            [sg.Button('Update')]]

window = sg.Window('My new window', layout)

while True:             # Event Loop
    event, values = window.Read()
    if event is None:
        break
    print(event)
    window['_TEXT_'].Update(values['_INPUT_']) #updats the value of _TEXT_ to be _INPUT_