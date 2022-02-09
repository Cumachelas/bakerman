import subprocess as sub
import time

dependencies = ["configparser",
                "pytest-shutil",
                "pysimplegui"]

errorstate = False

logfile = open("InstallerLog.txt", "w")
logfile.write("")
logfile = open("InstallerLog.txt", "a")

for i in dependencies:
    cmdout = sub.run("pip install " + i)
    time.sleep(10)
    if cmdout.returncode != 0:
        logfile.write("Failed to install dependency " + i + " (Return Code: " + str(cmdout.returncode))
        pass
    logfile.write(str(cmdout) + "\n")
    
print("Dependencies installed, quitting...")    

logfile.close()