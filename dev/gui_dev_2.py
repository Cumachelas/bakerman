import PySimpleGUI as sg

window = sg.Window('My Script',
                    [[sg.Text('Document to open')],
                    [sg.In(key="in"),
                     sg.FileBrowse()],
                    [sg.Open(), sg.Cancel()]])

event, values = window.read()

fname = values["in"]

sg.popup('The filename you chose was', fname)