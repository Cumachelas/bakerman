import PySimpleGUI as sg      

layout = [[sg.Text('Persistent window', key="writtenText")],      
          [sg.Input(key='-IN-')],      
          [sg.Button('Read'), sg.Exit()]]      

window = sg.Window('Window that stays open', layout)      

while True: 
    event, values = window.read() 
    print(event, values)
    window["writtenText"].update(values["-IN-"])       
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()