# BAKERMAN GUI 4compile v0.6 by Svjatoslav Skabarin; Release 13.01.2021

# Designed for Doughscript v2.1, but as of v0.2, only LED, WAIT, TEXT classes are implemented
# Doughskript syntax and functions: please reference ds_readme.txt

BAKERMAN_VERSION = "GUI 4compile v0.6"
DS_VERSION = "v2.1"

import configparser
import os
import re
import shutil
import sys
import time
from msvcrt import getch

import PySimpleGUI as GUI
from PySimpleGUI.PySimpleGUI import WIN_CLOSED

default_font = "Montserrat"

start_time = time.time()

doDebug = False # default, changing

def debugLog(log):
    if doDebug:
        timeDelta = time.time() - start_time
        log = str(round(timeDelta, 2)) + "s " + log + "\n"
        logFile.write(log)   

config = configparser.ConfigParser()
config.read('config/settings.ini')

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

window = GUI.Window(title="BAKERMAN v0.5 (w/ Bakery front end)",
                         element_justification = "left",
                         background_color="white",
                         layout=s, # from Bakery_GUI.py
                         icon=("assets/bakerman_icon_v1.ico"))

while True:

    event, value = window.read()
    
    if event == "Start encode":
    
        InputFilePath = str(value["InputFilePath"])
        OutputFilePath = str(value["OutputFilePath"])
        
        VerifyExecutionTimings = value["VerifyExecutionTimings"]
        doDebug = value["doDebug"] # fully-functional
        EnableVerboseLogging = value["EnableVerboseLogging"]
        
        break
        
    if event == "Quit" or event == WIN_CLOSED:
        
        window.close()
        exit(0)

if doDebug:
    
    if not os.path.isdir("logs"): os.makedirs("logs")
    
    LogFilePath = "logs/" + str(int(time.time())) + ".txt"
    logFile = open(LogFilePath, "a")

LED_PIN = config['bakerman_config']['LED_PIN']
LED_PIN = re.sub(pattern="\n", repl="", string=LED_PIN)
Button_PIN = config['bakerman_config']['Button_PIN']
Button_PIN = re.sub(pattern="\n", repl="", string=Button_PIN)

pretext = open("config/pretext.conf", "r") 
posttext = open("config/posttext.conf", "r")

output = open("temp/cache.ino", "w")
output.write("")
output = open("temp/cache.ino", "a") # TEMP - temp/write.temp

DoughLineCount = 0
line = 0
LED_ON = False
errorstate = False

#output functions and their definitions:

def run(i):

    cmd = i.replace("RUN ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "Keyboard.press(GUI_KEY);\nKeyboard.press('r');\nKeyboard.releaseAll;\ndelay(100);\nKeyboard.print(" + cmd + ");\nKeyboard.press(RETURN_KEY);\n"
    output.write(cmd)

def text(i): 

    cmd = i.replace("TEXT ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "\tKeyboard.print(" + cmd + ");\n"
    output.write(cmd)

def wait(i):

    cmd = i.replace("WAIT ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "\tdelay(" + cmd + ");\n"
    output.write(cmd)

def toggleLED():

    global LED_ON

    if LED_ON:
        cmd = "\tdigitalWrite(" + LED_PIN + ", LOW);\n"
        LED_ON = not LED_ON
    elif not LED_ON:
        cmd = "\tdigitalWrite(" + LED_PIN + ", HIGH);\n"
        LED_ON = not LED_ON

    output.write(cmd)
        
#############################################################

debugLog("Programm initialized")

dough = open(InputFilePath)

debugLog("File opened succesfully...")

cmd_list = dough.readlines()
totalLines = list.__len__(cmd_list)

output.write(pretext.read())

for i in cmd_list: #execution loop

    if "BREAK" in i:
        debugLog("BREAK called, stopped encoding")
        break

    elif "LED" in i: toggleLED()
        
    elif "TEXT" in i: text(i)
    
    elif "WAIT" in i: wait(i)

    elif "RUN" in i: run(i)

    else:
        debugLog("Unknown command in line " + str(line) + ". Quitting")
        errorstate = True
        break
        
    line = line + 1

output.write(posttext.read())

if errorstate:
    exit(0)
    
try:
    shutil.copyfile("temp/write.temp", OutputFilePath.encode('unicode_escape'))
except Exception as e:
    debugLog("Shutil copy failed with " + str(e))
    
    
debugLog("File written successfully to " + OutputFilePath)

debugLog("Program finished")

output.close()
pretext.close()
posttext.close()
logFile.close()