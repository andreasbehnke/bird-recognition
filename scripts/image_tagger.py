import termios, fcntl, sys, os

pictureViewer = "eog -w"
imageDirectory = sys.argv[1]

# - support command line argument for tag-key-mapping files
# - continue on keyboard input
# - load cvs file if exists
# - load available tag - key mapping
# - display tag - key mapping
# - add new line to cvs on key entry
# - skip existing tagged files
# - make sure csv is saved after each step

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
            if (f.endswith("jpg") | f.endswith("jpeg")):
                image = root +  "/" + f
                print image
                os.system(pictureViewer + " " + image + " &")
                c = sys.stdin.read(1)
                print "Got character", repr(c)
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
