#!/usr/bin/python3

import os

filePath = "/tmp/youtubeGUI.txt"
tempFile = open(filePath, "r+")
commandList = tempFile.readlines()
tempFile.close()
os.remove(filePath)

for cmd in commandList:
    os.system(cmd)
              

