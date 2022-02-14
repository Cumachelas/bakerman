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
__-> see ds_readme.txt__
