import termios
import fcntl
import sys
import os

pictureViewer = "eog -w"
imageDirectory = sys.argv[1]
labelsFileName = imageDirectory + "labels.csv"

# - continue on keyboard input
# - load available tag - key mapping
# - display tag - key mapping
# - add new line to cvs on key entry
# - make sure csv is saved after each step

# read labels from csv files
# create empty file if not exists
open(labelsFileName, 'a').close()
# read existing csv data to string for searching for existing files
csvData = ""
with open(labelsFileName, 'r') as labelsFile:
    csvData = labelsFile.read()

# Prepare terminal for single character input
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

# iterate over all images found in imageDirectory
try:
    for root, dirs, files in os.walk(imageDirectory):
        for f in files:
            if ((f.endswith("jpg") or f.endswith("jpeg")) and (csvData.find(f) == -1)):
                image = root +  "/" + f
                print image
                os.system(pictureViewer + " " + image + " &")
                c = sys.stdin.read(1)
                print "Got character", repr(c)
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
