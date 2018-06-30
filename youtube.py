#!/usr/bin/python3

import sys, pyperclip, subprocess, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class YoutubeGUI(QWidget):
    
    def __init__(self, parent = None):
        super(YoutubeGUI, self).__init__(parent)

        self.rootdir = os.path.dirname(os.path.realpath(__file__))
        self.videos = []

        self.shortcutDelete = QShortcut(QKeySequence("Del"), self)
        self.shortcutDelete.activated.connect(self.deleteVideo)
        
        self.shortcutMoveUp = QShortcut(QKeySequence("Ctrl+Up"), self)
        self.shortcutMoveUp.activated.connect(self.moveFileUp)
        self.shortcutMoveDown = QShortcut(QKeySequence("Ctrl+Down"), self)
        self.shortcutMoveDown.activated.connect(self.moveFileDown)
        
        self.errorMessage = QErrorMessage()
        
        self.lOptions = QLabel("Options")
        self.lOptions.setAlignment(Qt.AlignCenter)
        self.lwOptions = QListWidget()
        self.lwOptions.itemClicked.connect(self.changedOptions)
        
        self.lFiles = QLabel("Files")
        self.lFiles.setAlignment(Qt.AlignCenter)
        self.lwFiles = QListWidget()
        self.lwFiles.itemClicked.connect(self.changedFile)
        
        self.bStartAll = QPushButton("Start All")
        self.bStartAll.clicked.connect(self.clickedStartAll)

        self.bStartSelected = QPushButton("Start Selected")
        self.bStartSelected.clicked.connect(self.clickedStartSelected)
        
        self.bPaste = QPushButton("Paste")
        self.bPaste.clicked.connect(self.clickedPaste)
        
        self.lOutputPath = QLabel("Output Directory")
        self.leOutputPath = QLineEdit()
        self.leOutputPath.setText("/home/user/Videos")
        self.leOutputPath.textChanged.connect(self.changedleOutputPath)

        self.level0v = QVBoxLayout()
        self.splitter = QSplitter(Qt.Horizontal)

        self.level0v.addWidget(self.bPaste)

        self.rowButtons = QHBoxLayout()
        self.rowButtons.addWidget(self.bStartAll)
        self.rowButtons.addWidget(self.bStartSelected)
        self.level0v.addLayout(self.rowButtons)

        

        self.rowOutput = QHBoxLayout()
        self.rowOutput.addWidget(self.lOutputPath)
        self.rowOutput.addWidget(self.leOutputPath)
        self.level0v.addLayout(self.rowOutput)
        
        # Left side
        self.Left = QWidget()
        self.level3vLeft = QVBoxLayout()
        self.level3vLeft.addWidget(self.lOptions)
        self.level3vLeft.addWidget(self.lwOptions)
        #self.level2hLeft.addLayout(self.level3vLeft)
        self.Left.setLayout(self.level3vLeft)
        
        # Right side
        self.Right = QWidget()
        self.level3vRight = QVBoxLayout()
        self.level3vRight.addWidget(self.lFiles)
        self.level3vRight.addWidget(self.lwFiles)
        #self.level2hRight.addLayout(self.level3vRight)
        self.Right.setLayout(self.level3vRight)
        
        self.setWindowTitle("Youtube GUI")
        self.showMaximized()
        
        self.splitter.addWidget(self.Left)
        self.splitter.addWidget(self.Right)
        w = self.size().width()
        #h = self.size().height()
        self.splitter.setSizes([int(w * 0.4), int(w * 0.6)])
        self.level0v.addWidget(self.splitter)
        self.setLayout(self.level0v)
        
        
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'yt_icon_rgb.png'))


    def changedleOutputPath(self):
        if self.lwFiles.selectedItems():
            si = self.lwFiles.selectedItems()[0]
            i = self.lwFiles.indexFromItem(si).row()
            self.videos[i]["Output Path"] = self.leOutputPath.text()
            
    def moveFileUp(self):
        if self.lwFiles.selectedItems() and (len(self.lwFiles.selectedItems()) == 1):
            si = self.lwFiles.selectedItems()[0]
            i = self.lwFiles.indexFromItem(si).row()
            if i > 0:
                removedItem = self.lwFiles.takeItem(i)
                removedDict = self.videos[i]
                del self.videos[i]
                switchIndex = i - 1
                self.lwFiles.insertItem(switchIndex, removedItem)
                self.videos.insert(switchIndex, removedDict)
                for s in self.lwFiles.selectedItems():
                    self.lwFiles.setCurrentItem(s, QItemSelectionModel.Deselect)
                self.lwFiles.setCurrentItem(removedItem, QItemSelectionModel.Select)

    def moveFileDown(self):
        if self.lwFiles.selectedItems() and (len(self.lwFiles.selectedItems()) == 1):
            si = self.lwFiles.selectedItems()[0]
            i = self.lwFiles.indexFromItem(si).row()
            if i < self.lwFiles.count():
                removedItem = self.lwFiles.takeItem(i)
                removedDict = self.videos[i]
                del self.videos[i]
                switchIndex = i + 1
                self.lwFiles.insertItem(switchIndex, removedItem)
                self.videos.insert(switchIndex, removedDict)
                for s in self.lwFiles.selectedItems():
                    self.lwFiles.setCurrentItem(s, QItemSelectionModel.Deselect)
                self.lwFiles.setCurrentItem(removedItem, QItemSelectionModel.Select)

    def changedOptions(self):
        si = self.lwFiles.selectedItems()[0]
        indexFile = self.lwFiles.indexFromItem(si).row()
        si = self.lwOptions.selectedItems()[0]
        OptionName = si.text()
        indexOption = self.lwOptions.indexFromItem(si).row()
        
        code = self.videos[indexFile]["Options List"][indexOption]["Code"]
        #print(code)
        self.videos[indexFile]["Selected Code"] = code
        
    def changedFile(self):
        si = self.lwFiles.selectedItems()[0]
        i = self.lwFiles.indexFromItem(si).row()
        self.loadOptions(i)
        
        
    def clickedStartAll(self):
        filePath = "/tmp/youtubeGUI.txt"
        fo = open(filePath, "w")
        for d in self.videos:
            oPath = "\"{}/%(title)s.%(ext)s\"".format(d["Output Path"])
            fo.write("youtube-dl -f %s -o %s %s\n" % (d["Selected Code"], oPath, d["url"]))
        fo.close()
        app = "{}/RunCommands.py".format(self.rootdir)
        myKonsoleCommand = ["konsole", "-e", app]
        subprocess.Popen(myKonsoleCommand)

    def clickedStartSelected(self):
        if self.lwFiles.selectedItems():
            filePath = "/tmp/youtubeGUI.txt"
            fo = open(filePath, "w")
            
            for si in self.lwFiles.selectedItems():
                i = self.lwFiles.indexFromItem(si).row()
                oPath = "\"{}/%(title)s.%(ext)s\"".format(self.videos[i]["Output Path"])
                fo.write("youtube-dl -f %s -o %s %s\n" % (self.videos[i]["Selected Code"], oPath, self.videos[i]["url"]))
            fo.close()
            app = "{}/RunCommands.py".format(self.rootdir)
            myKonsoleCommand = ["konsole", "-e", app]
            subprocess.Popen(myKonsoleCommand)
        
    def clickedPaste(self):
        self.bPaste.setText("Loading")
        url = str(pyperclip.paste())
        if url[:4] == "http":
            cmdTitle = ["youtube-dl", "-e", url]
            pTitle = subprocess.Popen(cmdTitle, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            ilt = pTitle.communicate()
            
            cmdData = ["youtube-dl", "-F", "--youtube-skip-dash-manifest", url]
            pData = subprocess.Popen(cmdData, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            il = pData.communicate()
            
            pTitle.wait()
            pData.wait()
            self.bPaste.setText("Paste")
            
            title = str((ilt[0].splitlines())[0], 'utf-8')
            il = il[0].splitlines()
            infoList = []
            for b in il:
                infoList.append(str(b, 'utf-8'))
            infoList.reverse()
            
            
            
            self.videos.append({"Selected Code": "", "url": url, "Options List": [], "Output Path": self.leOutputPath.text(), "Title": title})
        
            for info in infoList:
                if info[0].isdigit():
                    x = info.split()
                    format_code = x[0]
                    extension = x[1]
                    details = info[24:]
                    ex = (extension + "     ")[:5]
                    details = ex + details
                    details = details.replace("audio only", "")
                    details = details.replace("DASH audio", "audio")
                    details = details.replace(" ,", ",")
                    self.videos[-1]["Options List"].append({"Code": format_code, "Details": details})
                
            if self.lwFiles.selectedItems():
                sel = self.lwFiles.selectedItems()
                for ss in sel:
                    self.lwFiles.setCurrentItem(ss, QItemSelectionModel.Deselect)
                
            self.videos[-1]["Selected Code"] = self.videos[-1]["Options List"][0]["Code"]
            lwItem = QListWidgetItem(title)
            self.lwFiles.addItem(lwItem)
            self.loadOptions(-1)
            self.lwFiles.setCurrentItem(lwItem, QItemSelectionModel.Select)
            
        else:
            self.errorMessage.showMessage("Not a URL")
        


    def deleteVideo(self):
        if self.lwFiles.selectedItems():
            self.lwOptions.clear()
            for si in self.lwFiles.selectedItems():
                i = self.lwFiles.indexFromItem(si).row()
                self.lwFiles.takeItem(i)
                del self.videos[i]
                
    def loadOptions(self, i):
        self.lwOptions.clear()

        for option in self.videos[i]["Options List"]:
            lwItem = QListWidgetItem(option["Details"])
            self.lwOptions.addItem(lwItem)
            if option["Code"] == self.videos[i]["Selected Code"]:
                self.lwOptions.setCurrentItem(lwItem, QItemSelectionModel.Select)

           
           
           
           
           
        

def main():
   app = QApplication(sys.argv)
   ex = YoutubeGUI()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
