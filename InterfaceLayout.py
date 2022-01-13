import PySimpleGUI as GUI

default_font = "Montserrat"

s = [[GUI.Text("Assign an input file",
                    font=(default_font, 12, "bold"),
                    background_color="white",
                    text_color="black")],
     
    [GUI.Text("(any .txt or .dough file, written in DS v2.1)",
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
    
    [GUI.Checkbox("Verify execution timings",
                    key="VerifyExecutionTimings",
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black")],
    
    [GUI.Checkbox("Create log files",
                    key="doDebug", # see settings.ini
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
    
    [GUI.Checkbox("Verbose logging/Debug",
                    key="EnableVerboseLogging",
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black")],
    
    [GUI.VerticalSeparator(pad=(0, 5), color="white")],
    
    [GUI.Text("Log",
                    font=(default_font, 12, "bold"),
                    background_color="white",
                    text_color="black")],
    
    [GUI.VerticalSeparator(pad=(0, 5), color="white")],
    
    [GUI.Multiline(key="logBox",
                    size=(50, 12),
                    font=(default_font, 12),
                    background_color="white",
                    text_color="black",
                    disabled=True)],
    ]


