# BAKERMAN v0.5 by Svjatoslav Skabarin; Release 09.01.2021

# Designed for Doughscript v2.1, but as of v0.2, only LED, WAIT, TEXT classes are implemented
# Doughskript syntax and functions: please reference ds_readme.txt

import configparser
import os
import re
import shutil
import sys
import time
from msvcrt import getch

start_time = time.time()

if not os.path.isdir("logs"): os.makedirs("logs")

config = configparser.ConfigParser()
config.read('config/settings.ini')

if config['bakerman_config']['doDebug'] in ["True", "true", "yes"]:
    doDebug = True
else: doDebug = False

LED_PIN = config['bakerman_config']['LED_PIN']
LED_PIN = re.sub(pattern="\n", repl="", string=LED_PIN)
Button_PIN = config['bakerman_config']['Button_PIN']
Button_PIN = re.sub(pattern="\n", repl="", string=Button_PIN)

pretext = open("config/pretext.conf", "r") 
posttext = open("config/posttext.conf", "r")

output = open("temp/write.temp", "w")
output.write("")
output = open("temp/write.temp", "a")

if doDebug:
    LogFilePath = "logs/" + str(int(time.time())) + ".txt"
    logFile = open(LogFilePath, "a")

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

def debugLog(log):
    if doDebug:
        timeDelta = time.time() - start_time
        log = str(round(timeDelta, 2)) + "s " + log + "\n"
        logFile.write(log)   

print("\n\n                  BAKERMAN                   ")
print("---------------------------------------------")
print("Kooky Bakerman v0.5 -- using Doughskript v2.1\n\n")

debugLog("Programm initialized")

while True: #input file loop
    try:
        dough = open(input("Enter DS source file path: "), 'r')
        break
    except FileNotFoundError:
        for backspaceTime1 in range(2):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        print("Invalid Path!")
        debugLog("Invalid input file entered")

print("File opened succesfully...\n")
time.sleep(1)

cmd_list = dough.readlines()
totalLines = list.__len__(cmd_list)

output.write(pretext.read())

for i in cmd_list: #execution loop

    print(str(line) + " " + i, end = "")

    if "BREAK" in i:
        print("\nBREAK or another interrupt issued, stopped at line", str(line), "of", str(totalLines), "total.")
        debugLog("BREAK called, stopped encoding")
        break

    elif "LED" in i: toggleLED()
        
    elif "TEXT" in i: text(i)
    
    elif "WAIT" in i: wait(i)

    elif "RUN" in i: run(i)

    else:
        print("\nUnknown command in line " + str(line) + ". Press f to pay respects and quit.")
        debugLog("Unknown command in line " + str(line) + ". Quitting")
        errorstate = True
        break
        
    line = line + 1

output.write(posttext.read())

output.close()
pretext.close()
posttext.close()

if errorstate:
    a = getch()
    exit(0)

else:
    while True: #output file loop

        inoName = input("\n\nEnter the .INO filename: ") + ".ino"

        if os.path.isfile(inoName):

            print("This file already exists. Overwrite? (y/n)")

            debugLog("Existent file detected: " + inoName)

            if input("--->") == "y":
                print("Overwriting file " + inoName + " and quitting session")
                break

            else:
                for backspaceTime2 in range(3):
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                continue

        else:
            print("Creating file " + inoName + " and quitting session")
            break
        
    shutil.copy("temp/write.temp", inoName)
    debugLog("File written successfully")

debugLog("Program finished")
