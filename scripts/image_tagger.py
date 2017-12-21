import termios
import sys
import os
import shutil
import time

pictureViewer = "eog -w"
imageDirectory = sys.argv[1]
labelsFileName = imageDirectory + "labels.csv"
tagMapFileName = imageDirectory + "tagmap.csv"

# - display tag - key mapping
# - add new line to cvs on key entry
# - use relative path to file, not absolute!

# read tagmap file
tags = {}
with open(tagMapFileName, 'r') as tagMapFile:
    line = tagMapFile.readline()
    while line:
        keyLabel = line.split(':')
        tags[keyLabel[0].strip()] = keyLabel[1].strip()
        line = tagMapFile.readline()

# read labels from csv files
# create empty file if not exists
open(labelsFileName, 'a').close()
# make a backup
shutil.copyfile(labelsFileName, labelsFileName + "." + str(time.time()) + ".bak")
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
            if (f.endswith("jpg") or f.endswith("jpeg")):
                if (csvData.find(f) != -1):
                    print "skipping tagged image " + f
                else:
                    image = root +  "/" + f
                    print image
                    os.system(pictureViewer + " " + image + " &")

                    # display available labelsFile
                    print "choose one of the following labels for this image or press RETURN for no label:"
                    for k in tags:
                        print k + " - " + tags[k]
                    c = sys.stdin.read(1)
                    print "Got character", repr(c)
                    with open(labelsFileName, 'a') as labels:
                        labels.write(c + "," + image + "\n")
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
