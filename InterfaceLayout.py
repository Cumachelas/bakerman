import PySimpleGUI as GUI

default_font = "Montserrat"

s = [[GUI.Text("Assign an input file",
                    font=(default_font, 12, "bold"),
                    background_color="white",
                    text_color="black")],
     
    [GUI.Text("(any .txt or .dough file, written in DS v3 or older)",
                    font=(default_font, 12, "italic"),
                    background_color="white",
                    text_color="black")],
    
    [GUI.Input(key="InputFilePath", pad=((0, 0), (0, 0)), expand_x=True),
    
    GUI.FileBrowse(button_text="Browse...",
                    file_types=(("Text files", ".txt"), ("Doughskript files", ".dough")),
                    button_color="black",
                    font=(default_font, 8))],
    
    [GUI.VerticalSeparator(pad=(0, 5), color="white")],
    
    [GUI.Text("Assign an output file",
                    font=(default_font, 12, "bold"),
                    background_color="white",
                    text_color="black")],
    
    [GUI.Text("(please keep the .ino filetype)",
                    font=(default_font, 12, "italic"),
                    background_color="white",
                    text_color="black")],
    
    [GUI.Input(key="OutputFilePath", pad=((0, 0), (0, 0)), expand_x=True),
    
    GUI.FileSaveAs(button_text="Save As...",
                    file_types=(("Arduino Sketches", ".ino"),),
                    button_color="black",
                    font=(default_font, 8))],
    
    [GUI.VerticalSeparator(pad=(0, 5), color="white")],
    
    [GUI.Text("Options",
                    font=(default_font, 12, "bold"),
                    background_color="white",
                    text_color="black")],
    
    [GUI.VerticalSeparator(pad=(0, 3), color="white")],
    
    [GUI.Text("Boot header time:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
     
    GUI.Input(key="BootHeaderTime",
              default_text="6.2",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 10), (0, 0))),
    
    GUI.Text("LED Pin:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
     
    GUI.Input(key="LedPin",
              default_text="1",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 10), (0, 0))),
    
    GUI.Text("Button pin:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
     
    GUI.Input(key="ButtonPin",
              default_text="2",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 10), (0, 0))),
    
    GUI.Text("Layout:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
    
    GUI.Combo(values=["German", "English"],
                default_value="German",
                background_color="white",
                button_background_color="white",
                button_arrow_color="black",
                font=(default_font, 10),
                auto_size_text=True,
                key="KeyboardLayout")],
    
    [GUI.VerticalSeparator(pad=(0, 3), color="white")],
    
    [GUI.Checkbox("Verify execution timings",
                    key="VerifyExecutionTimings",
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black")],
    
    [GUI.Checkbox("Create log files",
                    key="doDebug", # see settings.ini
                    default=True,
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black"),
     
     GUI.Button("Start encode",
                    pad = ((200, 0), (0, 0)),
                    button_color="black",
                    font=(default_font, 12)),
     
     GUI.Button("Quit",
                    pad = ((20, 0), (0, 0)),
                    button_color="black",
                    font=(default_font, 12))],
    
    [GUI.Checkbox("Auto-open Arduino IDE on completion",
                    key="OpenArduino",
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black")], 
       
    [GUI.VerticalSeparator(pad=(0, 5), color="white")]

    ]


