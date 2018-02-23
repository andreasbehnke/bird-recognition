import sys
import exifread
import shutil
import os

imageDirectory = sys.argv[1]
targetDirectory = sys.argv[2]
labelsFileName = imageDirectory + "labels.csv"

with open(labelsFileName, 'r') as labelsFile:
    line = labelsFile.readline()
    while line:
        labelFile = line.split(',')
        label = labelFile[0]
        src = imageDirectory + labelFile[1].strip()
        line = labelsFile.readline()
        dst = ""
        with open(src, 'rb') as fh:
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            dateTaken = str(tags["EXIF DateTimeOriginal"]).replace(':','-').replace(' ','_')
            if label == "":
                label = "nobird"
            #dst = targetDirectory + '/' + dateTaken +  '_' + label.replace(' ','') + '.jpg'
            dstPath = targetDirectory + '/' + label.replace(' ', '');
            dst = dstPath + '/' + dateTaken + '.jpg'
            print dst
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)
        shutil.copyfile(src, dst)
