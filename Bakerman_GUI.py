# BAKERMAN GUI v1.0.1 by Svjatoslav Skabarin; Release 09.02.2022

# Designed for Doughscript v3, but as of v1.0, only certain functions are implemented
# Doughskript syntax and functions: please reference ds_readme.txt

# Dependencies: InterfaceLayout.py, configparser, shutil, pysimplegui --- install with dep_install.py

BAKERMAN_VERSION = "v1.0.1 (w/BakeryGUI)"
DS_VERSION = "v3"

import configparser
import subprocess as sub
import math
import os
import re
import shutil
import sys
import time
#from msvcrt import getch # - deprecated

import PySimpleGUI as GUI
from PySimpleGUI.PySimpleGUI import WIN_CLOSED

from InterfaceLayout import s, default_font

q = '"'

start_time = time.time()

doDebug = False
headerPresent = False

def debugLog(log):
    if doDebug:
        timeDelta = time.time() - start_time
        log = str(round(timeDelta, 2)) + "s " + log + "\n"
        logFile.write(log)
        #sys.stdout.write(log + "\n") # - deprecated
        
def forGerman(string):
    debugLog("Coverting to German LAYOUT")
    string_rep = string.replace("/", "&")
    string_rep = string_rep.replace(":", ">")
    string_rep = string_rep.replace("y", "|")
    string_rep = string_rep.replace("z", "y")
    string_rep = string_rep.replace("|", "z")
    return string_rep

config = configparser.ConfigParser()
config.read('config/settings.ini')

window = GUI.Window(title="BAKERMAN " + BAKERMAN_VERSION,
                         element_justification = "left",
                         background_color="white",
                         layout=s, # from Bakery_GUI.py
                         icon=("assets/bakerman_icon_v1.ico"))

while True: #input/Window loop

    event, value = window.read()
    
    if event == "Start encode":
    
        InputFilePath = str(value["InputFilePath"])
        OutputFilePath = str(value["OutputFilePath"])
        
        VerifyExecutionTimings = value["VerifyExecutionTimings"]
        doDebug = value["doDebug"]
        SEAMLESS_MODE = value["SeamlessMode"]
        
        INO_BOOTTIME = float(value["BootHeaderTime"])
        if INO_BOOTTIME < 0: INO_BOOTTIME = 0
        
        LED_PIN = int(value["LedPin"])
        if LED_PIN < 1: LED_PIN = 1 #hard-default
        
        BUTTON_PIN = int(value["ButtonPin"])
        if BUTTON_PIN < 1: BUTTON_PIN = 2 #hard-default
        
        LAYOUT = value["KeyboardLayout"]
        std_delay = int(value["ExecutionTiming"])
        
        break
        
    if event == "Quit" or event == WIN_CLOSED:
        
        window.close()
        exit(0)

if doDebug: #debug setup
    
    if not os.path.isdir("logs"): os.makedirs("logs")
    
    LogFilePath = "logs/" + str(int(time.time())) + ".txt"
    logFile = open(LogFilePath, "a")

pretext = "#include<DigiKeyboard.h>\n\nvoid setup(){\n\n"
posttext = open("config/posttext.conf", "r")

output = open(OutputFilePath, "w")
output.write("")
output = open(OutputFilePath, "a")

DoughLineCount = 0
line = 1
LED_ON = False
errorstate = False

#output functions and their definitions:

def run(i):

    cmd = i.replace("RUN ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "\tDigiKeyboard.sendKeyStroke(KEY_R,MOD_GUI_LEFT); //RUN\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\tDigiKeyboard.print(" + q + forGerman(cmd) + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n"
    output.write(cmd)

def text(i): 

    cmd = i.replace("PRINT ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    output.write("\tDigiKeyboard.print(" + q + forGerman(cmd) + q + "); //PRINT\n\n")
    
def textln(i): 

    cmd = i.replace("PRINTLN ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    output.write("\tDigiKeyboard.println(" + q +  forGerman(cmd) + q + "); //PRINTLN\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def wait(i):

    wait_time = int(i.replace("WAIT ", "", 1))

    cmd = "\tDigiKeyboard.delay(" + str(wait_time*1000) + "); //WAIT\n\n"
    output.write(cmd)

def toggleLED():

    global LED_ON

    if LED_ON:
        cmd = "\tdigitalWrite(" + str(LED_PIN) + ", LOW); //LED ON\n\n"
        LED_ON = not LED_ON
    elif not LED_ON:
        cmd = "\tdigitalWrite(" + str(LED_PIN) + ", HIGH); //LED OFF\n\n"
        LED_ON = not LED_ON

    output.write(cmd)

def key(i):
    
    cmd = i.replace("KEY ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)
    
    if "ENTER" in i or "RETURN" in i:
        output.write("\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\n")
    elif "GUI" in i or "WIN" in i:
        output.write("\tDigiKeyboard.sendKeyStroke(MOD_GUI_LEFT);\n\n")
    else:
        output.write("\tDigiKeyboard.sendKeyStroke(" + cmd + ");\n\n")
        
def close():
    
    output.write("\tDigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT); //CLOSE\n\n")
            
#############################################################

debugLog("Programm initialized")

try:
    dough = open(InputFilePath)
except FileNotFoundError:
    debugLog("Source file not found")
    errorstate = True
    cmd_list = ["0"] #making sure, that STARTDELAY has a list to check
else:
    debugLog("File opened succesfully...")
    cmd_list = dough.readlines()
    totalLines = list.__len__(cmd_list)
    output.write(pretext)

if "STARTDELAY" in cmd_list[0] and not errorstate: #header-init
    
    debugLog("STARTDELAY-header found")
    headerPresent = True
    
    startdelay = int(cmd_list[0].replace("STARTDELAY ", "", 1))
    startdelay = startdelay-INO_BOOTTIME
    
    if startdelay > 0: output.write("\tdelay(" + str(math.floor(startdelay*1000)) + "); // STARTDELAY\n")
    
for i in cmd_list: #execution loop
    
    if errorstate: break

    if headerPresent and i == cmd_list[0]: pass
    
    elif "BREAK" in i:
        debugLog("BREAK called, stopped encoding")
        break

    elif "LED" in i: toggleLED()
    
    elif "KEY" in i: key(i)
    
    elif "PRINTLN" in i: textln(i)
    
    elif "PRINT" in i: text(i)
    
    elif "WAIT" in i: wait(i)

    elif "RUN" in i: run(i)
    
    elif "CLOSE" in i: close()
    
    elif "STARTDELAY" in i:
        debugLog("STARTDELAY encountered out of header, ignoring")

    else:
        debugLog("Unknown command in line " + str(line) + ". Quitting")
        errorstate = True
        break
        
    line = line + 1

output.write(posttext.read())

output.close()
posttext.close()

if errorstate:
    
    error = sys.exc_info()[1]
    
    if os.path.isfile(OutputFilePath): os.remove(OutputFilePath)
    
    GUI.Popup(title="Error encountered")
    exit(0)

SeamlessOutputFilePath = OutputFilePath.replace(os.path.basename(OutputFilePath), "") + os.path.basename(OutputFilePath).replace(".ino", "") + "/" + os.path.basename(OutputFilePath)
if SEAMLESS_MODE:
    os.mkdir(OutputFilePath.replace(os.path.basename(OutputFilePath), "") + os.path.basename(OutputFilePath).replace(".ino", ""))
    shutil.move(OutputFilePath, SeamlessOutputFilePath)
    debugLog("Seamless mode - opening IDE")
    os.startfile(SeamlessOutputFilePath)
    
debugLog("File written successfully to " + SeamlessOutputFilePath)

if doDebug: logFile.close()