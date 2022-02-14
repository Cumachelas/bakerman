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
              default_text="5.7",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 8), (0, 0)),
              tooltip="Initialization time of Digispark; Default: 5.7s"),
    
    GUI.Text("Execution timing:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
     
    GUI.Input(key="ExecutionTiming",
              default_text="220",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 8), (0, 0)),
              tooltip="Standard delay and execution speed. Depending on the system and application, set in range 80-400ms. Default: 220ms"),
    
    GUI.Text("LED Pin:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
     
    GUI.Input(key="LedPin",
              default_text="1",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 8), (0, 0)),
              tooltip="LED Pin on Digispark"),
    
    GUI.Text("Button pin:",
                    font=(default_font, 8),
                    background_color="white",
                    text_color="black"),
     
    GUI.Input(key="ButtonPin",
              default_text="2",
              font=(default_font, 10),
              size=(4, 1),
              pad=((0, 8), (0, 0)),
              tooltip="Button Pin on Digispark"),
    
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
    
    [GUI.Checkbox("Initialize first keystroke",
                    key="InitializeKeystroke",
                    default=True,
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black",
                    tooltip="Prevents missing the first input. Recommended.")],
    
    [GUI.Checkbox("Create log files",
                    key="doDebug",
                    default=False,
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black",
                    tooltip="Whether or not to create .txt logs."),
     
     GUI.Button("Start encode",
                    pad = ((300, 0), (0, 0)),
                    button_color="black",
                    font=(default_font, 12)),
     
     GUI.Button("Quit",
                    pad = ((20, 0), (0, 0)),
                    button_color="black",
                    font=(default_font, 12))],
    
    [GUI.Checkbox("Seamless mode",
                    key="SeamlessMode",
                    default=True,
                    font=(default_font, 10),
                    background_color="white",
                    text_color="black",
                    tooltip="Automatically creates sketch folder and launches Arduino IDE on successful compile. Recommended.")], 
       
    [GUI.VerticalSeparator(pad=(0, 5), color="white")]

    ]


