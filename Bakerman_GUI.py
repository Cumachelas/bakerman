# BAKERMAN GUI v0.7 by Svjatoslav Skabarin; Release 06.02.2022

# Designed for Doughscript v3, but as of v0.7, only certain functions are implemented
# Doughskript syntax and functions: please reference ds_readme.txt

#Dependancies: InterfaceLayout.py, configparser, msvcrt, shutil, re, time -- TODO: Dep. installer

BAKERMAN_VERSION = "v0.7 (w/BakeryGUI)"
DS_VERSION = "v3"

import configparser
import os
import re
import shutil
import sys
import time
from msvcrt import getch

import PySimpleGUI as GUI
from PySimpleGUI.PySimpleGUI import WIN_CLOSED

from InterfaceLayout import s, default_font

start_time = time.time()

doDebug = False # default, changing

def debugLog(log):
    if doDebug:
        timeDelta = time.time() - start_time
        log = str(round(timeDelta, 2)) + "s " + log + "\n"
        logFile.write(log)   

config = configparser.ConfigParser()
config.read('config/settings.ini')

window = GUI.Window(title="BAKERMAN " + BAKERMAN_VERSION,
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

LED_PIN = re.sub(pattern="\n", repl="", string=config['bakerman_config']['LED_PIN']) # CONFIG RECALL
Button_PIN = re.sub(pattern="\n", repl="", string=config['bakerman_config']['Button_PIN'])

#PRESS_CMD = TODO

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

    cmd = "DigiKeyboard.sendKeyStroke(GUI_KEY);\nDigiKeyboard.println('r');\nKeyboard.releaseAll;\nDigiKeyboard.delay(100);\nDigiKeyboard.println(" + cmd + ");\nDigiKeyboard.sendKeyStroke(RETURN_KEY);\n"
    output.write(cmd)

def text(i): 

    cmd = i.replace("TEXT ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "\tDigiKeyboard.println(" + cmd + ");\n"
    output.write(cmd)

def wait(i):

    cmd = i.replace("WAIT ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "\tDigiKeyboard.delay(" + cmd + ");\n"
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