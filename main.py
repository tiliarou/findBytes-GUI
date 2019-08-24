""" This code was rushed in about 24 hours. Expect bugs, and poor coding; and probably some other 
stuff too that I can't think of currently ¯\_(ツ)_/¯ . Besides all of that though, I hope you find the tool useful. Cheers """

#MESSAGE FOR AMAZINGCHZ (so I don't forget lol)
# YOU NEED TO CHANGE RELEASE TITLE AND SYNTAX.MD LINK EACH VERSION!!!!!
#----------------------------------------------------------------------

import sys
import time

try:
    import PyQt5
except:
    download = input("\nPyQt5 is not installed! Install now? (Y\\N) ")
    if download == "Y" or download == "y":
        #Python is weird; some python versions have pip one way; others have it a different...
        try:
            from pip._internal import main
            main(["install", "PyQt5"])
            del main
        except:
            import pip
            pip.main(["install", "PyQt5"])
            del pip
        
        import PyQt5
    elif download == "N" or download == "n":
        print("\n===Installation Aborted===\nProgram will now terminate...")
        time.sleep(3)
        sys.exit()
    else:
        print('\n"{0}" is an unknown option. Please only type "Y" or "N".\nProgram will now terminate...'.format(download))    
        time.sleep(3.5)
        sys.exit()

try:
    from github import Github
except:
    time.sleep(1)
    download = input("\nPyGithub is not installed! Install now? (Y\\N) ")
    if download == "Y" or download == "y":
        #Python is weird; some python versions have pip one way; others have it a different...
        try:
            from pip._internal import main
            main(["install", "PyGithub"])
            del main
        except:
            import pip
            pip.main(["install", "PyGithub"])
            del pip
        
        from github import Github
    elif download == "N" or download == "n":
        print("\n===Installation Aborted===\nProgram will now terminate...")
        time.sleep(3)
        sys.exit()
    else:
        print('\n"{0}" is an unknown option. Please only type "Y" or "N".\nProgram will now terminate...'.format(download))    
        time.sleep(3.5)
        sys.exit()

from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QPushButton

import ctypes
import subprocess
import io
import os

import urllib.request
import zipfile
import shutil

#Need this, in case user picks "find new offset from DIFFERENT files"
global counter
counter = 0

#Writing default option for user...
global oldFileHeader, newFileHeader
oldFileHeader = "Auto-Decide"
newFileHeader = "Auto-Decide"

f = open(".\\resources\\advanced\\oldFile.txt", "w")
f.write(oldFileHeader)
f.close()

f = open(".\\resources\\advanced\\newFile.txt", "w")
f.write(newFileHeader)
f.close()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        """Welcome UI"""
        global counter
        counter += 1
        if counter >= 2:
            self.close()
            x, y, width, height = self.getGeometry()
            counter = 1

        #Checking if user has downloaded findBytes.py
        self.findBytes("full")
               
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\startUp\\startUp.ui"), self)

        #Putting in try, as normally, start up UI doesn't get coordinates (only if user goes back "<- Home")
        try:
            self.setGeometry(x, y, width, height)
        except:
            pass

        self.Start.pressed.connect(self.startOldFile)
        self.githubBtn.pressed.connect(self.githubPage)

        self.show()

        #Declaring variables, to prevent future possible errors, later on.
        global oldFileDir, newFileDir
        oldFileDir = ""
        newFileDir = ""

        #Checking if there is new version of findBytes GUI
        self.checkForUpdate()

    def githubPage(self):
        os.system(self.resource_path(".\\resources\\findBytes-GUI_GitHub.bat"))
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def checkForUpdate(self):
        """Checks for new releases of findBytes GUI"""
        g = Github()

        g = g.get_repo("AmazingChz/findBytes-GUI")

        releases = g.get_releases()

        #Getting latest release...
        count = 0
        for release in releases:
            count += 1
            if count == 1:
                latest = release.title

        #Telling user there is a new release (if there is one)
        if latest != "Making things easier and faster...always.":
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Information)
            self.choice.setWindowTitle("New release is available...")
            self.choice.setText('There is a new version of findBytes GUI available!\n\nWould you like to view the latest release on GitHub?')
            self.choice.addButton(QMessageBox.Yes)
            self.choice.addButton(QMessageBox.No)
            result = self.choice.exec_()

            #Opening latest release for user (if they wish to see)
            if result == QMessageBox.Yes:
                os.system(self.resource_path(".\\resources\\findBytes-GUI_GitHub.bat"))

    def findBytes(self, process):
        """Makes sure user downloaded findBytes.py"""
        #Checking if user has downloaded findBytes.py
        findBytesExist = os.path.isfile(self.resource_path(".\\resources\\tools\\findBytes\\findBytes.py"))

        if process == "full":
            if findBytesExist == False:
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("findBytes.py is missing...")
                self.choice.setText('It looks like findBytes.py is not downloaded. Download now?\n\nNote: if not downloaded, program will terminate.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.addButton(QMessageBox.Cancel)
                result = self.choice.exec_()

                if result == QMessageBox.Ok:
                    #Putting in try, because who knows what can happen lol
                    try:
                        path = urllib.request.urlretrieve("https://gist.github.com/3096/ffd6d257f148aab0b74bfc50dfe43e80/archive/9b46f05d72d8c292f1fecd67be9b8dfbf1645189.zip", "9b46f05d72d8c292f1fecd67be9b8dfbf1645189.zip")

                        #Unzipping findBytes.py...
                        zip_ref = zipfile.ZipFile(str(path[0]), 'r')
                        zip_ref.extractall(self.resource_path(".\\resources\\tools\\findBytes\\"))
                        zip_ref.close()

                        #Deleting zip file...
                        os.system("del " + str(path[0]))

                        #Copying findBytes.py out of folder...
                        os.system("copy " + self.resource_path(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189\\findBytes.py") + " " + self.resource_path(".\\resources\\tools\\findBytes\\"))

                        #Deleting old folder...
                        #1) Deleting contents of folder
                        #2) Deleting actual folder itself
                        p = os.popen("del " + self.resource_path(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189"), "w")
                        p.write("Y")

                        shutil.rmtree(self.resource_path(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189"), ignore_errors=False, onerror=None)

                        os.system("cls")
                        
                        #Telling user findBytes.py was downloaded...
                        self.choice = QMessageBox()
                        self.choice.setIcon(QMessageBox.Information)
                        self.choice.setWindowTitle("findBytes.py was successfully downloaded...")
                        self.choice.setText('findBytes.py was successfully downloaded! You may now continue to use this program...')
                        self.choice.setStandardButtons(QMessageBox.Ok)
                        self.choice.exec_()

                    except:
                        #Telling user findBytes.py failed to download...
                        self.choice = QMessageBox()
                        self.choice.setIcon(QMessageBox.Critical)
                        self.choice.setWindowTitle("findBytes.py failed to downloaded...")
                        self.choice.setText('findBytes.py could not be downloaded. If the problem persists, please contact @AmazingChz#5695 on Discord.\n\nTry again?\n\nNote: if you do not try again, the program will terminate.')
                        self.choice.addButton(QPushButton("Try Again"), QMessageBox.YesRole)
                        self.choice.addButton(QMessageBox.Cancel)
                        result = self.choice.exec_()
                        if result == 0:
                            self.findBytes("part")
                        else:
                            sys.exit()
                else:
                    sys.exit()
                    
        if process == "part":
            #Putting in try, because who knows what can happen lol
            try:
                path = urllib.request.urlretrieve("https://gist.github.com/3096/ffd6d257f148aab0b74bfc50dfe43e80/archive/9b46f05d72d8c292f1fecd67be9b8dfbf1645189.zip", "9b46f05d72d8c292f1fecd67be9b8dfbf1645189.zip")

                #Unzipping findBytes.py...
                zip_ref = zipfile.ZipFile(str(path[0]), 'r')
                zip_ref.extractall(self.resource_path(".\\resources\\tools\\findBytes\\"))
                zip_ref.close()

                #Deleting zip file...
                os.system("del " + str(path[0]))

                #Copying findBytes.py out of folder...
                os.system("copy " + self.resource_path(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189\\findBytes.py") + " " + self.resource_path(".\\resources\\tools\\findBytes\\"))

                #Deleting old folder...
                #1) Deleting contents of folder
                #2) Deleting actual folder itself
                p = os.popen("del " + self.resource_path(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189"), "w")
                p.write("Y")

                shutil.rmtree(self.resource_path(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189"), ignore_errors=False, onerror=None)

                #Telling user findBytes.py was downloaded...
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Information)
                self.choice.setWindowTitle("findBytes.py was successfully downloaded...")
                self.choice.setText('findBytes.py was successfully downloaded! You may now continue to use this program...')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()

            except:
                #Telling user findBytes.py failed to download...
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Critical)
                self.choice.setWindowTitle("findBytes.py failed to downloaded...")
                self.choice.setText('findBytes.py could not be downloaded. If the problem persists, please contact @AmazingChz#5695 on Discord.\n\nTry again?\n\nNote: if you do not try again, the program will terminate.')
                self.choice.addButton(QPushButton("Try Again"), QMessageBox.YesRole)
                self.choice.addButton(QMessageBox.Cancel)
                result = self.choice.exec_()
                if result == 0:
                    self.findBytes("part")
                else:
                    sys.exit()

    def getGeometry(self):
        """Gets location of Window, so when user loads new UI, it stays there."""
        coordinates = str(self.geometry())
        coordinates = coordinates[19:]
        coordinates = coordinates[:len(coordinates) - 1]
       
        split = coordinates.split(",")
       
        x = float(split[0])
        y = float(split[1])
        width = float(split[2])
        height = float(split[3])

        return float(x), float(y), float(width), float(height)

    def startOldFile(self):
        """Loads the UI that asks for user's old file (the one they have the offset for)"""
        x, y, width, height = self.getGeometry()
        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\oldFile\\oldFile.ui"), self)
        self.setGeometry(x, y, width, height)

        self.home.pressed.connect(self.__init__)
        self.here.pressed.connect(self.newWindowNSO)
        self.advanced.pressed.connect(self.advOld)
        self.newFile.pressed.connect(self.selectOldFile)
        self.Next.pressed.connect(self.startNewFile)


        self.show()

    def selectOldFile(self):
        """Asks user to open their old file (the one they already have the offset for)"""
        global oldFileDir
        self.oldFileDir, self.oldFileExtension = QFileDialog.getOpenFileName(self,"Select OLD File...", "","Decompressed Yaz0 (*.uncompressed)")
        oldFileDir = str(self.oldFileDir)
        
        self.oldFileName = QFileInfo(self.oldFileDir).fileName()

        self.plainTextEdit.setPlainText(self.oldFileDir)

    def startNewFile(self):
        """Loads the UI that asks for the new file (the one they want to port their patch to)"""
        #Putting in try, as user has option to come back to this screen if they want. Without try, this would cause an error
        # Makes sure all info is filled out on-screen
        try:
            if str(self.plainTextEdit.toPlainText()) == "":
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("Is everything filled out?")
                self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()

            else:
                #Checking which radio button was clicked [old file]
                f = open(self.resource_path(".\\resources\\advanced\\oldFile.txt"), "r")
                global oldFileHeader
                oldFileHeader = str(f.read())
                f.close()

                if oldFileHeader == "Auto-Decide":
                    with open(self.oldFileDir, 'rb') as f:
                        hexdata = str(f.read().hex())

                    #Checking if "main.nso" has *.NSO header or not...
                    if hexdata[0:8] == "4E534F30" or hexdata[0:8] == "4e534f30" or hexdata[0:11] == "4E 53 4F 30" or hexdata[0:11] == "4e 53 4f 30":
                        oldFileHeader = "Has *.NSO Header."
                    else:
                        oldFileHeader = "Doesn't Have *.NSO Header."

                #Removing header (if file has header)...
                if oldFileHeader == "Has *.NSO Header.":
                    self.oldRemoveHeader = self.resource_path(".\\resources\\temp\\") + str(self.oldFileName)

                    with open(self.oldFileDir, 'rb') as in_file:
                        with open(self.oldRemoveHeader, 'wb') as out_file:
                            out_file.write(in_file.read()[100:])
                    
                x, y, width, height = self.getGeometry()
                self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\newFile\\newFile.ui"), self)
                self.setGeometry(x, y, width, height)

                self.back.pressed.connect(self.startOldFile)
                self.here.pressed.connect(self.newWindowNSO)
                self.newFile.pressed.connect(self.selectNewFile)
                self.advanced.pressed.connect(self.advNew)
                self.Next.pressed.connect(self.getMultOffsets)


                self.show()
        except:
            x, y, width, height = self.getGeometry()
            self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\newFile\\newFile.ui"), self)
            self.setGeometry(x, y, width, height)

            self.back.pressed.connect(self.startOldFile)
            self.here.pressed.connect(self.newWindowNSO)
            self.newFile.pressed.connect(self.selectNewFile)
            self.advanced.pressed.connect(self.advNew)
            self.Next.pressed.connect(self.getMultOffsets)


            self.show()

    def selectNewFile(self):
        """Asks user to open their new file (the one they want to port their offset to)"""
        global newFileDir
        self.newFileDir, self.newFileExtension = QFileDialog.getOpenFileName(self,"Select NEW File...", "","Decompressed Yaz0 (*.uncompressed)")
        newFileDir = str(self.newFileDir)

        self.newFileName = QFileInfo(self.newFileDir).fileName()

        self.plainTextEdit.setPlainText(self.newFileDir)

    def getMultOffsets(self):
        """Allows user to put as many offsets as they'd like in findBytes GUI"""
        #We need to use a "try" block, for if the user picks "find new offset from SAME files", the program doesn't crash
        try:
            # Makes sure all info is filled out on-screen
            if str(self.plainTextEdit.toPlainText()) == "":
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("Is everything filled out?")
                self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()

            else:
                #Putting in "try" block, since user has option to get new offset from SAME files later on. This would cause an error without this "try".
                try:
                    #Checking which radio button was clicked [new file]
                    f = open(self.resource_path(".\\resources\\advanced\\newFile.txt"), "r")
                    global newFileHeader
                    newFileHeader = str(f.read())
                    f.close()

                    if newFileHeader == "Auto-Decide":
                        with open(self.newFileDir, 'rb') as f:
                            hexdata = str(f.read().hex())

                        #Checking if "main.nso" has *.NSO header or not...
                        if hexdata[0:8] == "4E534F30" or hexdata[0:8] == "4e534f30" or hexdata[0:11] == "4E 53 4F 30" or hexdata[0:11] == "4e 53 4f 30":
                            newFileHeader = "Has *.NSO Header."
                        else:
                            newFileHeader = "Doesn't Have *.NSO Header."

                    #Removing header (if file has header)...
                    if newFileHeader == "Has *.NSO Header.":
                        self.newRemoveHeader = self.resource_path(".\\resources\\temp\\") + str(self.newFileName)

                        with open(self.newFileDir, 'rb') as in_file:
                            with open(self.newRemoveHeader, 'wb') as out_file:
                                out_file.write(in_file.read()[100:])
                except:
                    pass

                x, y, width, height = self.getGeometry()
                self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\getMultipleOffsets\\getMultipleOffsets.ui"), self)
                self.setGeometry(x, y, width, height)

                self.back.pressed.connect(self.startNewFile)
                self.Settings.pressed.connect(self.settings)
                self.howTo.pressed.connect(self.howToMultipleOffsets)
                self.choose.pressed.connect(self.pchtxt)
                self.Next.pressed.connect(self.multOffsetsParsing)

                self.show()
        except:
            #Putting in "try" block, since user has option to get new offset from SAME files later on. This would cause an error without this "try".
            try:
                #Checking which radio button is checked [new file]
                f = open(self.resource_path(".\\resources\\advanced\\newFile.txt"), "r")
                newFileHeader = str(f.read())
                f.close()

                if newFileHeader == "Auto-Decide":
                    with open(self.newFileDir, 'rb') as f:
                        hexdata = str(f.read().hex())

                    #Checking if "main.nso" has *.NSO header or not...
                    if hexdata[0:8] == "4E534F30" or hexdata[0:8] == "4e534f30" or hexdata[0:11] == "4E 53 4F 30" or hexdata[0:11] == "4e 53 4f 30":
                        newFileHeader = "Has *.NSO Header."
                    else:
                        newFileHeader = "Doesn't Have *.NSO Header."

                #Removing header (if file has header)...
                if newFileHeader == "Has *.NSO Header.":
                    self.newRemoveHeader = self.resource_path(".\\resources\\temp\\") + str(self.newFileName)

                    with open(self.newFileDir, 'rb') as in_file:
                        with open(self.newRemoveHeader, 'wb') as out_file:
                            out_file.write(in_file.read()[100:])
            except:
                pass

            x, y, width, height = self.getGeometry()
            self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\getMultipleOffsets\\getMultipleOffsets.ui"), self)
            self.setGeometry(x, y, width, height)

            self.back.pressed.connect(self.startNewFile)
            self.Settings.pressed.connect(self.settings)
            self.howTo.pressed.connect(self.howToMultipleOffsets)
            self.choose.pressed.connect(self.pchtxt)
            self.Next.pressed.connect(self.multOffsetsParsing)

            self.show()

    def pchtxt(self):
        """Gets user' *.pchtxt file and ports all patches [OPTIONAL] (IPSwitch)"""
        # Loading UI...
        x, y, width, height = self.getGeometry()
        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\pchtxt\\pchtxt.ui"), self)
        self.setGeometry(x, y, width, height)

        self.show()

        self.pchtxtFileDir, self.pchtxtFileExtension = QFileDialog.getOpenFileName(self,"Select PATCH File...", "","Patch File (*.pchtxt)")
        self.pchtxtFileDir = str(self.pchtxtFileDir)
        self.pchtxtFileName = QFileInfo(self.pchtxtFileDir).fileName()

        # Making sure user actually selected a *.pchtxt file...
        if self.pchtxtFileDir in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVQXYZ":
            self.getMultOffsets()
            return

        ###

        os.system("python" + " " + self.resource_path("./resources/tools/parserIPS/parserIPS.py") +  " " + self.pchtxtFileDir)

        #Porting offsets via findbytes.py...
        #Clearing screen (if there is anything on it)...
        offsets = open(self.resource_path(".\\resources\\tools\\parserIPS\\resources\\offsets.txt"), "r")
        os.system("cls")
        #Calculating how many dashes to fit with the file name...
        dashes = 96 + len(str(self.pchtxtFileName))
        print(('-' * dashes) + '\n' + 
              '| This will take quite some time depending on how many offsets "{0}" contains. Please be patient! |'.format(self.pchtxtFileName) +
              '\n' + ('-' * dashes) + '\n')
               
        counter = 1
        self.ported = []
        for line in offsets:
            newLine = False
            if line == "\n":
                self.ported.append("\n")
            else:
                try:
                    #Putting in try, as last offset may not have "\n"...
                    try:
                        fixedOffset = line.split("\n")
                        lineOffset = fixedOffset[0]
                        newLine = True
                    except:
                        lineOffset = str(line)
                      
                    #Makes sure line isn't empty (I know this is poorly written, but whatever lol...
                    if (lineOffset.startswith("0") or lineOffset.startswith("1") or lineOffset.startswith("2")
                        or lineOffset.startswith("3") or lineOffset.startswith("4") or lineOffset.startswith("5")
                        or lineOffset.startswith("6") or lineOffset.startswith("7") or lineOffset.startswith("8")
                        or lineOffset.startswith("9") or lineOffset.startswith("A") or lineOffset.startswith("B")
                        or lineOffset.startswith("C") or lineOffset.startswith("D") or lineOffset.startswith("E")
                        or lineOffset.startswith("F") or lineOffset.startswith("a") or lineOffset.startswith("b")
                        or lineOffset.startswith("c") or lineOffset.startswith("d") or lineOffset.startswith("e")
                        or lineOffset.startswith("f")):

                        cmd = str("python " + self.resource_path(".\\resources\\tools\\findBytes\\findBytes.py") + " " + str(self.oldRemoveHeader) + " " + str(self.newRemoveHeader) + " " + str(lineOffset))
                        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                        finalOutput = p.stdout.read()
                        retcode = p.wait()
                        finalOutput = str(finalOutput)
                        finalOutput = finalOutput[2:len(finalOutput) - 5]
                        self.ported.append(finalOutput)

                        #Telling user how many are ported...
                        if counter == 1:
                            print("1 offset (potentially) ported.")
                        else:
                            print("{0} offsets (potentially) ported.".format(counter))

                        counter += 1

                    #Adding new line if needed...
                    if newLine == True:
                        self.ported.append("\n")
                except:
                   continue
                                                                                                                        
        print("\n" + "--------------------------------------------------------------------------" + '\n' + 
              '| All done! Check findBytes GUI\'s screen to see your new ported offsets! |' +
              '\n' + "--------------------------------------------------------------------------" + '\n')

        offsets.close()

        x, y, width, height = self.getGeometry()
        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\pchtxtAllDone\\pchtxtAllDone.ui"), self)
        self.setGeometry(x, y, width, height)

        self.options.pressed.connect(self.userOptions)

        # Adding new offsets and new patches to screen
        # Adding patches...
        self.patches = []
        file = open(self.resource_path(".\\resources\\tools\\parserIPS\\resources\\patches.txt"))
        # Making sure that the number of items in self.patches == self.ported...
        for line in file:
            if line == "\n":
                self.patches.append("\n")
            else:
                try:
                    altPatch = line.split("\n")
                    altPatch = altPatch[0]

                    self.patches.append(altPatch)
                    self.patches.append("\n")
                except:
                    self.patches.append(line)

        file.close()

        failed = False
        for items in range(len(self.ported)):
            portedOffset = self.ported[items]
            if len(portedOffset) >= 3:
                altPortedOffset = portedOffset[0:8]

                if str(portedOffset[0]) == "-":
                    failed = True
                    self.userNewPatches.insertPlainText("*FAILED*" + " " + str(self.patches[items]))# + "\n")
                else:
                    try:
                        confidenceLevel = self.ported[items]
                        confidence = confidenceLevel.find("// Confidence level: ")
                        confidenceLevel = confidenceLevel[int(confidence):len(confidenceLevel)]
                
                        self.userNewPatches.insertPlainText(str(altPortedOffset) + " " + str(self.patches[items]) + " " + str(confidenceLevel))# + "\n")
                    except:
                        continue
            else:
                try:
                    self.userNewPatches.insertPlainText(str(portedOffset))# + " " + str(self.patches[items]))# + " " + str(confidenceLevel) + "\n")
                except:
                    continue

        if failed == True:
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Warning)
            self.choice.setWindowTitle("Failed to port...")
            self.choice.setText('One or more of your offsets could not be ported. These offsets have been replaced with "*FAILED*".')
            self.choice.setStandardButtons(QMessageBox.Ok)
            self.choice.exec_()

        #print("patches: {0}".format(self.patches))

        #print(self.ported)

        '''for items in range(len(self.patches)):
            print(self.patches[items])'''
        
        self.show()

        #self.plainTextEdit.setPlainText(self.pchtxtFileDir)

    def multOffsetsParsing(self):
        """Multiple Offsets Parsing"""
        #Making sure info is filled out...
        if self.offsets.toPlainText() == "":
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Warning)
            self.choice.setWindowTitle("Is everything filled out?")
            self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
            self.choice.setStandardButtons(QMessageBox.Ok)
            self.choice.exec_()
        else:
            self.oldOffsets = []
            self.patches = []
                
            #Writing all offsets that were given from user
            file = io.open(self.resource_path(".\\resources\\offsets\\offsets.txt"), "w", encoding="utf-8")
            text = self.offsets.toPlainText()
            file.write(text)
            file.close()

            #Reading the offsets
            hexCheckOffset = True
            hexCheckOffsetSpace = True
            file = io.open(self.resource_path(".\\resources\\offsets\\offsets.txt"), "r", encoding="utf-8")
            for lines in file.readlines():
                try:
                    tokens = lines.split(" ")
                    self.oldOffsets.append(tokens[0])

                    #Making sure offset is a valid hex number...
                    try:
                        int(tokens[0], 16)
                    except:
                        if tokens[0] == "":
                            hexCheckOffsetSpace = False
                        else:
                            hexCheckOffset = False
                except:
                    continue
            file.close()

            #Reading the patches
            hexCheckPatch = True
            file = io.open(self.resource_path(".\\resources\\offsets\\offsets.txt"), "r", encoding="utf-8")
            for lines in file.readlines():
                try:
                    tokens = lines.split(" ")
                    #Adding all patches to self.patches...
                    global patch
                    patch = ""
                    for items in range(len(tokens)):
                        try:
                            patch += " " + str(tokens[items + 1])
                        except:
                            continue
                    self.patches.append(patch)

                    #Making sure patch is a valid patch...
                    try:
                        str(patch)
                    except:
                        hexCheckPatch = False
                except:
                    continue
            file.close()

            #Checking if any offset is a space (" ")...
            if hexCheckOffsetSpace == False:
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("Found empty lines...")
                self.choice.setText('It looks like you have empty spaces/lines scattered across your offsets/patches. Please remove these unnecessary spaces/lines first, before proceeding.\n\nIf the problem persists, click the "HOW TO" button at the top right of this screen, then click the "Syntax Tutorial" in the middle.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()
            else:
                #Checking if user entered valid offsets/patches...
                if hexCheckOffset == False and hexCheckPatch == False:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Invalid hex digits and patches...")
                    self.choice.setText('One or more of your offsets and patches are not invalid.\n\nPlease make sure you typed your offsets and patches in correctly, then try again.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                elif hexCheckOffset == False:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Invalid hex digits...")
                    self.choice.setText('One or more of your offsets do not have valid hex digits.\n\nPlease make sure you typed your offsets in correctly, then try again.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                elif hexCheckPatch == False:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Invalid patches...")
                    self.choice.setText('One or more of your patches is not valid.\n\nPlease make sure you typed your patches in correctly, then try again.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                else:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Information)
                    self.choice.setWindowTitle("This may take awhile...")
                    self.choice.setText("It may take a few minutes to port all of your offsets. The time needed depends on how many offsets you are currently porting.\n\nThis program may freeze and stop working. Do not worry, this is normal; just be patient.")
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.addButton(QMessageBox.Cancel)
                    returnValue = self.choice.exec_()

                    if returnValue == QMessageBox.Cancel:
                        pass
                    else:
                        #Making sure user has findBytes.py downloaded...
                        self.findBytes("full")

                        #Porting the offsets via findBytes.py
                        self.ported = []
                        for items in range(len(self.oldOffsets)):
                            try:
                                fixedOffset = self.oldOffsets[items].split("\n")
                                self.oldOffsets[items] = fixedOffset[0]
                                    
                                cmd = str("python " + self.resource_path(".\\resources\\tools\\findBytes\\findBytes.py") + " " + str(self.oldRemoveHeader) + " " + str(self.newRemoveHeader) + " " + str(self.oldOffsets[items]))
                                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                                finalOutput = p.stdout.read()
                                retcode = p.wait()
                                finalOutput = str(finalOutput)
                                finalOutput = finalOutput[2:len(finalOutput) - 5]
                                self.ported.append(finalOutput)
                            except:
                                continue

                        #Removing "\n", etc. from old patches
                        for items in range(len(self.patches)):
                            try:
                                fixedOffset = self.patches[items].split("\n")
                                self.patches[items] = fixedOffset[0]
                            except:
                                continue

                        #Checking if user did not supply patches (at all)
                        if len(self.patches) <= 0:
                            while len(self.patches) != len(self.oldOffsets):
                                for items in range(len(self.oldOffsets)):
                                    self.patches.insert(0, " ")

                        #Calling final UI function woo!
                        self.allDoneMultipleOffsets()

    def allDoneMultipleOffsets(self):
        """Final UI for those who are porting multiple offsets/patches"""
        x, y, width, height = self.getGeometry()
        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\multAllDone\\multAllDone.ui"), self)
        self.setGeometry(x, y, width, height)

        failed = False
        
        #Adding old offsets and patches to screen
        for items in range(len(self.oldOffsets)):
            try:
                self.userOldPatches.insertPlainText(str(self.oldOffsets[items]) + " " + str(self.patches[items]) + "\n")
            except:
                continue

        #Adding new offsets and new patches to screen
        for items in range(len(self.ported)):
            try:
                portedOffset = self.ported[items]
                portedOffset = portedOffset[0:8]

                if str(portedOffset[0]) == "-":
                    failed = True
                    self.userNewPatches.insertPlainText("*FAILED*" + " " + str(self.patches[items]) + "\n")
                else:
                    confidenceLevel = self.ported[items]
                    confidenceLevel = confidenceLevel[9:len(confidenceLevel)]
                
                    self.userNewPatches.insertPlainText(str(portedOffset) + " " + str(self.patches[items]) + " " + str(confidenceLevel) + "\n")
            except:
                continue

        if failed == True:
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Warning)
            self.choice.setWindowTitle("Failed to port...")
            self.choice.setText('One or more of your offsets could not be ported. These offsets have been replaced with "*FAILED*".')
            self.choice.setStandardButtons(QMessageBox.Ok)
            self.choice.exec_()

        self.options.pressed.connect(self.userOptions)

        self.show()

    #Functions that create Secondary Windows

    def newWindowNSO(self):
        self.window = decompressNSO()
        self.window.show()

    def advOld(self):
        self.window = advancedOld()
        self.window.show()

    def advNew(self):
        self.window = advancedNew()
        self.window.show()

    def newWindowOffsetTut(self):
        self.window = offsetTut()
        self.window.show()

    def creditWin(self):
        self.window = credit()
        self.window.show()

    def offsetConversions(self):
        self.window = convertOffset()
        self.window.show()

    def howToMultipleOffsets(self):
        self.window = multOffsetsHelp()
        self.window.show()

    def settings(self):
        self.window = fileSettings()
        self.window.show()

    def userOptions(self):
        self.window = finalOptions(self)
        self.window.show()
        

    #############################################

    def quitProgram(self):
        """Quits program"""
        sys.exit()


# Secondary Windows [ex. The Button "here" creates one of these]

class decompressNSO(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(decompressNSO, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\decompressNSOInstructions\\decompressNSOInstructions.ui"), self)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class advancedOld(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(advancedOld, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\oldFile\\advanced.ui"), self)

        global oldFileHeader
        if oldFileHeader == "Auto-Decide":
            self.automatic.setChecked(True)
        elif oldFileHeader == "Has *.NSO Header.":
            self.header.setChecked(True)
        elif oldFileHeader == "Doesn't Have *.NSO Header.":
            self.noHeader.setChecked(True)

        self.question.pressed.connect(self.ques)
        self.save.pressed.connect(self.saveOld)

        self.ui.setFixedSize(self.ui.size())

        self.show()

    def closeEvent(self, event):
        #"Holder" variable in case user doesn't save their settings (by pressing "X")...
        global oldFileHeader
        #Checks if user didn't change their settings...
        if self.automatic.isChecked() and oldFileHeader == "Auto-Decide" or self.header.isChecked() and oldFileHeader == "Has *.NSO Header." or self.noHeader.isChecked() and oldFileHeader == "Doesn't Have *.NSO Header.":
            self.showDialog = False
        else:
            self.showDialog = True

        if self.showDialog == True:
            reply = QMessageBox.warning(
                self, "You forgot to save your settings!",
                "Would you like to save your settings, before closing this window?",
                QMessageBox.Save | QMessageBox.Close)

            if reply == QMessageBox.Close:
                #Telling user their settings were NOT saved...
                QMessageBox.critical(
                    self, "Settings NOT saved",
                    "Your settings were NOT saved.",
                    QMessageBox.Ok)
                event.accept()
            else:
                #Saving user's settings...
                self.close()
                self.saveOld()

        else:
            event.accept()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def saveOld(self):
        """Writes user's option into .\\resources\\advanced\\oldFile.txt"""
        global oldFileHeader
        if self.header.isChecked():
            oldFileHeader = "Has *.NSO Header."
        elif self.noHeader.isChecked():
            oldFileHeader = "Doesn't Have *.NSO Header."
        else:
            oldFileHeader = "Auto-Decide"

        f = open(".\\resources\\advanced\\oldFile.txt", "w")
        f.write(oldFileHeader)
        f.close()

        #Tells findBytes GUI to not show warning message about not saving your settings...
        self.showDialog = False

        QMessageBox.information(
                self, "Settings saved!",
                "Your settings were successfully saved!",
                QMessageBox.Ok)

        self.close()

    def ques(self):
        self.window = questionAuto()
        self.window.show()

class advancedNew(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(advancedNew, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\newFile\\advanced.ui"), self)

        global newFileHeader
        if newFileHeader == "Auto-Decide":
            self.automatic.setChecked(True)
        elif newFileHeader == "Has *.NSO Header.":
            self.header.setChecked(True)
        elif newFileHeader == "Doesn't Have *.NSO Header.":
            self.noHeader.setChecked(True)

        self.question.pressed.connect(self.ques)
        self.save.pressed.connect(self.saveNew)

        self.ui.setFixedSize(self.ui.size())

        self.show()

    def closeEvent(self, event):
        #"Holder" variable in case user doesn't save their settings (by pressing "X")...
        global newFileHeader
        #Checks if user didn't change their settings...
        if self.automatic.isChecked() and newFileHeader == "Auto-Decide" or self.header.isChecked() and newFileHeader == "Has *.NSO Header." or self.noHeader.isChecked() and newFileHeader == "Doesn't Have *.NSO Header.":
            self.showDialog = False
        else:
            self.showDialog = True

        if self.showDialog == True:
            reply = QMessageBox.warning(
                self, "You forgot to save your settings!",
                "Would you like to save your settings, before closing this window?",
                QMessageBox.Save | QMessageBox.Close)

            if reply == QMessageBox.Close:
                #Telling user their settings were NOT saved...
                QMessageBox.critical(
                    self, "Settings NOT saved",
                    "Your settings were NOT saved.",
                    QMessageBox.Ok)
                event.accept()
            else:
                #Saving user's settings...
                self.close()
                self.saveNew()

        else:
            event.accept()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def saveNew(self):
        """Writes user's option into .\\resources\\advanced\\newFile.txt"""
        global newFileHeader
        if self.header.isChecked():
            newFileHeader = "Has *.NSO Header."
        elif self.noHeader.isChecked():
            newFileHeader = "Doesn't Have *.NSO Header."
        else:
            newFileHeader = "Auto-Decide"

        f = open(".\\resources\\advanced\\newFile.txt", "w")
        f.write(newFileHeader)
        f.close()

        #Tells findBytes GUI to not show warning message about not saving your settings...
        self.showDialog = False

        QMessageBox.information(
                self, "Settings saved!",
                "Your settings were successfully saved!",
                QMessageBox.Ok)

        self.close()

    def ques(self):
        self.window = questionAuto()
        self.window.show()

class questionAuto(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(questionAuto, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\question\\question.ui"), self)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class offsetTut(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(offsetTut, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\offsetInstructions\\offsetInstructions.ui"), self)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class credit(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(credit, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\credits\\credits.ui"), self)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class convertOffset(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(convertOffset, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\convertOffset\\convertOffset.ui"), self)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class multOffsetsHelp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(multOffsetsHelp, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\multipleOffsetsInstructions\\multipleOffsetsInstructions.ui"), self)

        self.syntax.pressed.connect(self.loadTutorial)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def loadTutorial(self):
        os.system('start "" https://github.com/AmazingChz/findBytes-GUI/blob/6.0/syntax.md')

class fileSettings(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(fileSettings, self).__init__(*args, **kwargs)

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\fileSettings\\fileSettings.ui"), self)

        global oldFileDir, newFileDir, oldFileHeader, newFileHeader

        self.oldFileSet.setText(str(oldFileDir) + " --- " + oldFileHeader)
        self.newFileSet.setText(str(newFileDir) + " --- " + newFileHeader)

        self.ui.adjustSize()

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class finalOptions(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(finalOptions, self).__init__(*args, **kwargs)

        self.arguments = args[0]

        self.ui = loadUi(self.resource_path(".\\resources\\interfaces\\options\\options.ui"), self)

        self.offsetConversions.pressed.connect(self.offsetCon)
        self.sameFiles.pressed.connect(self.getSameFilesOffset)
        self.differentFiles.pressed.connect(self.getDifferentFilesOffset)
        self.quit.pressed.connect(self.quitProgram)
        self.credits.pressed.connect(self.creditProgram)

        self.show()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def offsetCon(self):
        self.window = convertOffset()
        self.window.show()

    def getSameFilesOffset(self):
        self.close()
        self.arguments.getMultOffsets()

    def getDifferentFilesOffset(self):
        self.close()
        self.arguments.startOldFile()

    def quitProgram(self):
        sys.exit()

    def creditProgram(self):
        self.window = credit()
        self.window.show()


#########################################################################################

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    #Hiding console :P
    #should only be uncommented, when compiling...
    """whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)"""
        
    #Checking if user wants to decompress *.NSO
    if len(sys.argv) == 2:
        os.system(resource_path(".\\resources\\tools\\hactool\\hactool") + " -t nso {0} --uncompressed={0}.uncompressed".format(sys.argv[1]))
        sys.exit()
    else:
        #Running normal findBytes GUI
        app = QApplication([])
        main_window = MainWindow()
        app.exec_()