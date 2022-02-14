**Kooky Bakerman by @Cumachelas**


DON'T USE THE EXECUTABLE DISTRIBUTION YET! 
_(testing purposes only)_


Installation and use:
  
  1. Clone this repository
  2. Make sure to have the latest version of Python v3.x installed 
  3. Run dep_install.py to get all the dependencies with pip (check logfile.txt for potential errors - better installer coming soon)
  4. Run Bakerman_GUI.py to convert DS files into executable Arduino code :-)

Use with Digispark (16MHz):

  1. Get the latest version of Arduino IDE (https://www.arduino.cc/en/software)
  2. Install the extended version of DigisparkKeyboard (https://github.com/ernesto-xload/DigisparkKeyboard)
  3. Install the Digistump drivers (https://github.com/digistump/DigistumpArduino/releases/download/1.6.7/Digistump.Drivers.zip)
  4. Add Digistump boards to your Arduino IDE: Preferences -> Additional Board URLs -> add http://digistump.com/package_digistump_index.json
  5. Select the correct board and the micronucleus programmer
  6. Upload the generated .ino file and THEN plug in your board (you will see a prompt from micronucleus)
  7. Have fun!


**Doughskript V3 - Syntax**

&& any[]
-> Comment, is ignored at any point in the code.

STARTDELAY int[s]
-> Waits given seconds minus the boot-up time. Only usable in the first line of a DS.

WAIT int[s]
-> Waits given seconds and proceeds with the execution.

:LOOP:
-> The void loop switches the interperation of DS into loop() of Arduino code. Usable once.

LOOP: int[iterations]
:LOOP
-> For-style loop. Runs the at the initialization given amount of times.

BREAK
-> Stops encoding and ignores any following code.
-> Not needed, but recommended as the last line of a DS.

KEY str[key1],str[key2],str[keyn]
-> Executes buton press(-es). Does NOT have automatic timing.
-> Accepts keycodes, full names and shortcuts like CTRL, ENTER, etc.

PRINT str[text]
-> Types the given text.

PRINTLN str[text]
-> Types the given text and presses Enter. Useful for executing commands.
-> Does NOT have built-in automatic timing.

CMDLN str[command]
-> Executes a given command in the Command Promt.

CMD
-> Opens the Command Promt.

RUN
-> Runs an expression in the Windows Run dialogue.

LEARN str[text]
-> Automatically saves the given text into the clipboard.
-> USE WITH CAUTION (may cause data loss).

PASTE
-> Pastes using the CTRL-V shortcut.

COPY
-> Copies using the CTRL-C shortcut.

SAVE
-> Saves using the CTRL-S shortcut.

SAVEAS str[filename]
-> Saves using the CTRL-S shortcut and a given name. 
-> Make sure to only use this when sure, that the Save As... dialogue will come up.

PRTSC
-> Takes a screenshot of the whole screen without any processing.

EXPLORER
-> Opens Windows explorer

DESKTOP
-> Minimizes all windows and shows Desktop.

CLOSE
-> Closes the currently active window.

LED
-> Toggles the state of the LED on the Digispark. Uses pin given during compile.