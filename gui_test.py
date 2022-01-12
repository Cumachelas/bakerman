import PySimpleGUI as GUI

default_font = "Montserrat" # -> config file

s = [[GUI.Text("1) Assign an input file",
                    font=(default_font, 24),
                    background_color="white",
                    text_color="black")],
    [GUI.Text("(any .txt or .dough file, written in DS v2.1)",
                    font=(default_font, 12, "italic"),
                    background_color="white",
                    text_color="black")],
    [GUI.FileBrowse(button_text="Browse...",
                    file_types=(("Doughskript files", ".dough"), ("Text files", ".txt")),
                    button_color="black",
                    font=(default_font, 12),
                    key="InputFileKey")],
    [GUI.Text()],
    [GUI.Submit(), GUI.Cancel()]]

firstWindow = GUI.Window(title="BAKERMAN v0.5 (w/ Bakery front end)",
                         element_justification = "left",
                         background_color="white",
                         layout=s,
                         margins=(200, 200),
                         icon=("assets/bakerman_icon_v1.ico"))

event, values = firstWindow.read()

firstWindow.close()

print(values["InputFileKey"])