# BAKERMAN GUI v1.1.9 by Svjatoslav Skabarin; Release 02.03.2022

# Designed for Doughscript v3.2, and as of v1.1.9, all features except for the MOUSE function are implemented
# Doughskript syntax and functions: please reference ds_readme.txt

# COMING IN RELEASE v1.2 -> full mouse support; German layout overhaul; instantaneous Digispark boot; major bugfixes

# Dependencies: InterfaceLayout.py, configparser, shutil, pysimplegui --- install with dep_install.py

BAKERMAN_VERSION = "v1.1.9 (w/BakeryGUI)"
DS_VERSION = "v3.2"

import configparser
import subprocess as sub
import math
import os
import re
import shutil
import sys
import time

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

def forGerman(string):
    
    string_rep = string.replace("/", "&")
    string_rep = string_rep.replace(":", ">")
    string_rep = string_rep.replace("-", "ß")
    
    string_rep = string_rep.replace("y", "|~")
    string_rep = string_rep.replace("z", "y")
    string_rep = string_rep.replace("|~", "z")
    string_rep = string_rep.replace("Y", "~|")
    string_rep = string_rep.replace("Z", "Y")
    string_rep = string_rep.replace("~|", "Z")
    
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
        INITIALIZE = value["InitializeKeystroke"]
        
        INO_BOOTTIME = float(value["BootHeaderTime"])
        if INO_BOOTTIME < 0: INO_BOOTTIME = 0
        
        LED_PIN = int(value["LedPin"])
        if LED_PIN < 1: LED_PIN = 1 #hard-default
        
        BUTTON_PIN = int(value["ButtonPin"])
        if BUTTON_PIN < 1: BUTTON_PIN = 2 #hard-default
        
        LAYOUT = value["KeyboardLayout"]
        
        std_delay = int(value["ExecutionTiming"])
        if std_delay < 48: std_delay = 50
        
        break
        
    if event == "Quit" or event == WIN_CLOSED:
        
        window.close()
        exit(0)

if doDebug: #debug setup
    
    if not os.path.isdir("logs"): os.makedirs("logs")
    
    LogFilePath = "logs/" + str(int(time.time())) + ".txt"
    logFile = open(LogFilePath, "a")

posttext = open("config/posttext.conf", "r")

output = open(OutputFilePath, "w")
output.write("")
output = open(OutputFilePath, "a")

line = 1

LED_ON = False
errorstate = False
forLoop = False
voidLoop = False

jiggleForm = "Line"
jigFactor = 5

needsMouse = False

#output functions and their definitions:

def loop(i):
    
    global voidLoop, forLoop, loopStart
    
    if ":LOOP:" in i:
        
        if not voidLoop:
            debugLog("Void loop initiated")
            voidLoop = True
            output.write("}\n\nvoid loop(){\n\n")
            
        else:
            debugLog("Void loop initiated twice, ignoring")
            
    elif "LOOP:" in i:
        
        debugLog("Beginning For-loop")
        forLoop = True
        loopStart = line
        
        n = int(i.replace("LOOP: ", "", 1))
        output.write("\tfor (int n = 0; n < " + str(n) + "; n++){ //LOOP\n\n")
            
    elif ":LOOP" in i:
        
        debugLog("Ending For-loop")
        forLoop = False
            
        output.write("}\n\n")
        
def cmdln(i):
    
    cmd = i.replace("CMDLN ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)
    
    output.write("\tDigiKeyboard.sendKeyStroke(KEY_R,MOD_GUI_LEFT); //CMDLN\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\tDigiKeyboard.print(" + q + "cmd" + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\tDigiKeyboard.print(" + q + forGerman(cmd) + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\n")

def cmda():
    
    output.write("\tDigiKeyboard.sendKeyStroke(KEY_R,MOD_GUI_LEFT); //CMD\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\tDigiKeyboard.print(" + q + "cmd" + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def run(i):

    cmd = i.replace("RUN ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    cmd = "\tDigiKeyboard.sendKeyStroke(KEY_R,MOD_GUI_LEFT); //RUN\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\tDigiKeyboard.print(" + q + forGerman(cmd) + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n"
    output.write(cmd)
    
def close(): output.write("\tDigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT); //CLOSE\n\tDigiKeyboard.delay(" + str(std_delay*0.75) + ");\n\n")
    
def desktop(): output.write("\tDigiKeyboard.sendKeyStroke(KEY_D,MOD_GUI_LEFT); //DESKTOP\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def prtsc(): output.write("\tDigiKeyboard.sendKeyStroke(70, MOD_GUI_LEFT); //PRTSC\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def explorer(): output.write("\tDigiKeyboard.sendKeyStroke(KEY_E, MOD_GUI_LEFT); //EXPLORER\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def paste(): output.write("\tDigiKeyboard.sendKeyStroke(KEY_V, MOD_CONTROL_LEFT); //PASTE\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def copy(): output.write("\tDigiKeyboard.sendKeyStroke(KEY_C, MOD_CONTROL_LEFT); //COPY\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def save(): output.write("\tDigiKeyboard.sendKeyStroke(KEY_S, MOD_CONTROL_LEFT); //SAVE\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def saveas(i):
    
    cmd = i.replace("SAVEAS ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)
    
    output.write("\tDigiKeyboard.sendKeyStroke(KEY_S, MOD_CONTROL_LEFT); //SAVEAS\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\ttDigiKeyboard.print(" + q + cmd + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\tDigiKeyboard.delay(" + str(std_delay) + ");\n\n")

def learn(i):
    
    t = i.replace("LEARN ", "", 1)
    t = re.sub(pattern="\n", repl="", string=t)
    
    output.write("\tDigiKeyboard.sendKeyStroke(0, MOD_GUI_LEFT); //CLIPBOARD LEARN\n\tDigiKeyboard.delay(" + str(std_delay*0.5) + ");\n\tDigiKeyboard.print(" + q + forGerman(t) + q + ");\n\tDigiKeyboard.sendKeyStroke(KEY_A,MOD_CONTROL_LEFT);\n\tDigiKeyboard.sendKeyStroke(KEY_C,MOD_CONTROL_LEFT);\n\tDigiKeyboard.sendKeyStroke(41);\n\n")

def text(i): 

    cmd = i.replace("PRINT ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    output.write("\tDigiKeyboard.print(" + q + forGerman(cmd) + q + "); //PRINT\n\n")
    
def textln(i): 

    cmd = i.replace("PRINTLN ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)

    output.write("\tDigiKeyboard.print(" + q +  forGerman(cmd) + q + "); //PRINTLN\n\tDigiKeyboard.sendKeyStroke(KEY_ENTER);\n\n")

def wait(i):

    cmd = i.replace("WAIT ", "", 1)
    wait_time = float(re.sub(pattern="\n", repl="", string=cmd))
    
    cmd = "\tDigiKeyboard.delay(" + str(wait_time*1000) + "); //WAIT\n\n"
    output.write(cmd)

def toggleLED():

    global LED_ON

    if LED_ON:
        cmd = "\tdigitalWrite(" + str(LED_PIN) + ", LOW); //LED OFF\n\n"
        LED_ON = not LED_ON
    elif not LED_ON:
        cmd = "\tdigitalWrite(" + str(LED_PIN) + ", HIGH); //LED ON\n\n"
        LED_ON = not LED_ON

    output.write(cmd)

def key(i):
    
    comb = ""
    
    cmd = i.replace("KEY ", "", 1)
    cmd = re.sub(pattern="\n", repl="", string=cmd)
    
    if ", " in cmd: key_list = cmd.split(", ")
    else: key_list = cmd.split(",")

    debugLog(str(key_list))
    
    for key in key_list:
        if "ENTER" in key or "RETURN" in key:
            comb = comb + "KEY_ENTER,"
        elif "GUI" in key or "WIN" in key:
            comb = comb + "MOD_GUI_LEFT,"
        elif "PRTSC" in key:
            comb = comb + "70,"
        elif "SHIFT" in key:
            comb = comb + "MOD_SHIFT_LEFT,"
        elif "ALT" in key:
            comb = comb + "MOD_ALT_LEFT,"
        elif "CTRL" in key or "CONTROL" in key:
            comb = comb + "MOD_CONTROL_LEFT,"
        else:
            comb = comb + key + ","
    
    output.write("\tDigiKeyboard.sendKeyStroke(" + comb.rstrip(",") + ");\n\n")
    
def comment(i):
    
    cmd = i.replace("&& ", "", 1)
    output.write("\t// " + re.sub(pattern="\n", repl="", string=cmd) + "\n\n")
    
def jiggle():
    
    global jiggleForm
    
    if jiggleForm == "Line":
        output.write("\tDigiMouse.moveY(10); //JIGGLER\n\tDigiMouse.delay(" + str(std_delay*jigFactor) + ");\n\tDigiMouse.moveY(-10);\n\tDigiMouse.delay(" + q + str(std_delay*jigFactor) + q + ");\n\n")
            
#############################################################

debugLog("Programm initialized")

try: dough = open(InputFilePath)
    
except FileNotFoundError:
    
    debugLog("Source file not found")
    errorstate = True
    cmd_list = ["0"] #making sure, that STARTDELAY has a list to check
    
else:
    
    debugLog("File opened succesfully...")
    cmd_list = dough.readlines()
    totalLines = list.__len__(cmd_list)
    
    if "JIGGLE" in dough or "MOUSE" in dough: #add all functions that use DigiMouse.h here
        needsMouse = True
        output.write("#include<DigiKeyboard.h>\n#include<DigiMouse.h>\n\nvoid setup(){\n\n")
    else:
        output.write("#include<DigiKeyboard.h>\n\nvoid setup(){\n\n")

if "STARTDELAY" in cmd_list[0] and not errorstate: #header-init
    
    debugLog("STARTDELAY-header found")
    headerPresent = True
    
    startdelay = int(cmd_list[0].replace("STARTDELAY ", "", 1))
    startdelay = startdelay-INO_BOOTTIME
    
    if startdelay > 0: output.write("\tdelay(" + str(math.floor(startdelay*1000)) + "); // STARTDELAY\n\n")
    
if INITIALIZE and not errorstate: 
    
    if needsMouse: output.write("\tDigiKeyboard.sendKeyStroke(0);\n\tDigiMouse.begin();\n\n")
    else: output.write("\tDigiKeyboard.sendKeyStroke(0);\n\n")  
    
for i in cmd_list: #execution loop
    
    if errorstate: break

    if headerPresent and i == cmd_list[0]: pass
    
    elif i == "\n":
        debugLog("Empty line detected, passing")
        pass
    
    elif "&&" in i: comment(i)
    
    elif "BREAK" in i:
        debugLog("BREAK called, stopped encoding")
        break
    
    elif "LOOP" in i: loop(i)

    elif "LED" in i: toggleLED()
    
    elif "KEY" in i: key(i)
    
    elif "PRINTLN" in i: textln(i)
    
    elif "PRINT" in i: text(i)
    
    elif "WAIT" in i: wait(i)
    
    elif "DESKTOP" in i: desktop()
    
    elif "PRTSC" in i: prtsc()
    
    elif "PASTE" in i: paste()
    
    elif "COPY" in i: copy()
    
    elif "LEARN" in i: learn(i)
    
    elif "SAVE" in i: save()
    
    elif "SAVEAS" in i: saveas()
    
    elif "EXPLORER" in i: explorer()

    elif "RUN" in i: run(i)
    
    elif "CMDLN" in i: cmdln(i)
    
    elif "CMD" in i: cmda()
    
    elif "CLOSE" in i: close()
    
    elif "JIGGLE" in i: jiggle()
    
    elif "STARTDELAY" in i:
        debugLog("STARTDELAY encountered out of header, ignoring")

    else:
        debugLog("Unknown command in line " + str(line) + ". Quitting")
        errorstate = True
        break
        
    line = line + 1

if voidLoop: output.write("}")
else: output.write(posttext.read())

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