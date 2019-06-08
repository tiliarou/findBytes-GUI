""" This code was rushed in about 24 hours. Expect bugs, and poor coding; and probably some other 
stuff too that I can't think of currently ¯\_(ツ)_/¯ . Besides all of that though, I hope you find the tool useful. Cheers """

import PyQt5
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QPushButton

import subprocess
import sys
import os
import time
import io

import urllib.request
import zipfile
import shutil

from github import Github

#Need this, in case user picks "find new offset from DIFFERENT files"
global counter
counter = 0

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
        self.ui = loadUi(".\\resources\\interfaces\\startUp\\startUp.ui", self)

        #Putting in try, as normally, start up UI doesn't get coordinates (only if user goes back "<- Home")
        try:
            self.setGeometry(x, y, width, height)
        except:
            pass

        self.Start.pressed.connect(self.startOldFile)

        self.show()

        #Declaring variables, to prevent future possible errors, later on.
        self.oldFileDir = ""
        self.newFileDir = ""

        self.oldFileHeader = ""
        self.newFileHeader = ""

        #Checking if there is new version of findBytes GUI
        self.checkForUpdate()

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
        if latest != "I don't like bugs, so I fixed them :>":
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Information)
            self.choice.setWindowTitle("New release is available...")
            self.choice.setText('There is a new version of findBytes-GUI available!\n\nWould you like to view the latest release on GitHub?')
            self.choice.addButton(QMessageBox.Yes)
            self.choice.addButton(QMessageBox.No)
            result = self.choice.exec_()

            #Opening latest release for user (if they wish to see)
            if result == QMessageBox.Yes:
                os.system(".\\resources\\findBytes-GUI_GitHub.bat")

    def findBytes(self, process):
        """Makes sure user downloaded findBytes.py"""
        #Checking if user has downloaded findBytes.py
        findBytesExist = os.path.isfile(".\\resources\\tools\\findBytes\\findBytes.py")

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
                        zip_ref.extractall(".\\resources\\tools\\findBytes\\")
                        zip_ref.close()

                        #Deleting zip file...
                        os.system("del " + str(path[0]))

                        #Copying findBytes.py out of folder...
                        os.system("copy .\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189\\findBytes.py .\\resources\\tools\\findBytes\\")

                        #Deleting old folder...
                        #1) Deleting contents of folder
                        #2) Deleting actual folder itself
                        p = os.popen("del .\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189", "w")
                        p.write("Y")

                        shutil.rmtree(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189", ignore_errors=False, onerror=None)

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
                zip_ref.extractall(".\\resources\\tools\\findBytes\\")
                zip_ref.close()

                #Deleting zip file...
                os.system("del " + str(path[0]))

                #Copying findBytes.py out of folder...
                os.system("copy .\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189\\findBytes.py .\\resources\\tools\\findBytes\\")

                #Deleting old folder...
                #1) Deleting contents of folder
                #2) Deleting actual folder itself
                p = os.popen("del .\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189", "w")
                p.write("Y")

                shutil.rmtree(".\\resources\\tools\\findBytes\\ffd6d257f148aab0b74bfc50dfe43e80-9b46f05d72d8c292f1fecd67be9b8dfbf1645189", ignore_errors=False, onerror=None)

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
        self.ui = loadUi(".\\resources\\interfaces\\oldFile\\oldFile.ui", self)
        self.setGeometry(x, y, width, height)

        self.home.pressed.connect(self.__init__)
        self.here.pressed.connect(self.newWindowNSO)
        self.newFile.pressed.connect(self.selectOldFile)
        self.Next.pressed.connect(self.startNewFile)


        self.show()

    def selectOldFile(self):
        """Asks user to open their old file (the one they already have the offset for)"""
        self.oldFileDir, self.oldFileExtension = QFileDialog.getOpenFileName(self,"Select OLD File...", "","Decompressed Yaz0 (*.uncompressed)")
        
        self.oldFileName = QFileInfo(self.oldFileDir).fileName()

        self.plainTextEdit.setPlainText(self.oldFileDir)

    def startNewFile(self):
        """Loads the UI that asks for the new file (the one they want to port their patch to)"""
        #Putting in try, as user has option to come back to this screen if they want. Without try, this would cause an error
        # Makes sure all info is filled out on-screen
        try:
            checkHeader = self.header.isChecked()
            checkNoHeader = self.noHeader.isChecked()
            if str(self.plainTextEdit.toPlainText()) == "" or checkHeader == False and checkNoHeader == False:
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("Is everything filled out?")
                self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()

            else:
                #Checking which radio button was clicked [old file]
                if self.header.isChecked():
                    self.oldFileHeader = "Has *.NSO Header."

                    self.oldRemoveHeader = ".\\resources\\temp\\" + str(self.oldFileName)

                    with open(self.oldFileDir, 'rb') as in_file:
                        with open(self.oldRemoveHeader, 'wb') as out_file:
                            out_file.write(in_file.read()[100:])

                elif self.noHeader.isChecked():
                    self.newFileHeader = "Doesn't Have *.NSO Header."
                    
                x, y, width, height = self.getGeometry()
                self.ui = loadUi(".\\resources\\interfaces\\newFile\\newFile.ui", self)
                self.setGeometry(x, y, width, height)

                self.back.pressed.connect(self.startOldFile)
                self.here.pressed.connect(self.newWindowNSO)
                self.newFile.pressed.connect(self.selectNewFile)
                self.Next.pressed.connect(self.getOffset)


                self.show()
        except:
            x, y, width, height = self.getGeometry()
            self.ui = loadUi(".\\resources\\interfaces\\newFile\\newFile.ui", self)
            self.setGeometry(x, y, width, height)

            self.back.pressed.connect(self.startOldFile)
            self.here.pressed.connect(self.newWindowNSO)
            self.newFile.pressed.connect(self.selectNewFile)
            self.Next.pressed.connect(self.getOffset)


            self.show()

    def selectNewFile(self):
        """Asks user to open their new file (the one they want to port their offset to)"""
        self.newFileDir, self.newFileExtension = QFileDialog.getOpenFileName(self,"Select NEW File...", "","Decompressed Yaz0 (*.uncompressed)")

        self.plainTextEdit.setPlainText(self.newFileDir)

    def getOffset(self):
        """Asks user for their old offset, which will then be ported to their new version file"""
        #We need to use a "try" block, for if the user picks "find new offset from SAME files", the program doesn't crash
        try:
            # Makes sure all info is filled out on-screen
            checkHeader = self.header.isChecked()
            checkNoHeader = self.noHeader.isChecked()
            if str(self.plainTextEdit.toPlainText()) == "" or checkHeader == False and checkNoHeader == False:
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("Is everything filled out?")
                self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()

            else:
                self.newFileName = QFileInfo(self.newFileDir).fileName()
                #Putting in "try" block, since user has option to get new offset from SAME files later on. This would cause an error without this "try".
                try:
                    #Checking which radio button is checked [new file]
                    if self.header.isChecked():
                        self.newFileHeader = "Has *.NSO Header."

                        self.newRemoveHeader = ".\\resources\\temp\\" + str(self.newFileName)

                        with open(self.newFileDir, 'rb') as in_file:
                            with open(self.newRemoveHeader, 'wb') as out_file:
                                out_file.write(in_file.read()[100:])

                    elif self.noHeader.isChecked():
                        self.newFileHeader = "Doesn't Have *.NSO Header."
                except:
                    pass

                x, y, width, height = self.getGeometry()
                self.ui = loadUi(".\\resources\\interfaces\\getOffset\\getOffset.ui", self)
                self.setGeometry(x, y, width, height)

                self.back.pressed.connect(self.startNewFile)
                self.here.pressed.connect(self.newWindowOffsetTut)
                self.Next.pressed.connect(self.allDone)
                self.multipleOffsets.pressed.connect(self.getMultOffsets)

                self.oldFileSet.setText(str(self.oldFileDir) + "; " + self.oldFileHeader)
                self.newFileSet.setText(str(self.newFileDir) + "; " + self.newFileHeader)

                self.show()
        except:
            self.newFileName = QFileInfo(self.newFileDir).fileName()
            #Putting in "try" block, since user has option to get new offset from SAME files later on. This would cause an error without this "try".
            try:
                #Checking which radio button is checked [new file]
                if self.header.isChecked():
                    self.newFileHeader = "Has *.NSO Header."

                    self.newRemoveHeader = ".\\resources\\temp\\" + str(self.newFileName)

                    with open(self.newFileDir, 'rb') as in_file:
                        with open(self.newRemoveHeader, 'wb') as out_file:
                            out_file.write(in_file.read()[100:])

                elif self.noHeader.isChecked():
                    self.newFileHeader = "Doesn't Have *.NSO Header."
            except:
                pass

            x, y, width, height = self.getGeometry()
            self.ui = loadUi(".\\resources\\interfaces\\getOffset\\getOffset.ui", self)
            self.setGeometry(x, y, width, height)

            self.back.pressed.connect(self.startNewFile)
            self.here.pressed.connect(self.newWindowOffsetTut)
            self.Next.pressed.connect(self.allDone)
            self.multipleOffsets.pressed.connect(self.getMultOffsets)

            self.oldFileSet.setText(str(self.oldFileDir) + "; " + self.oldFileHeader)
            self.newFileSet.setText(str(self.newFileDir) + "; " + self.newFileHeader)

            self.show()

    def getMultOffsets(self):
        """Allows user to put as many offsets as they'd like in findBytes GUI"""
        x, y, width, height = self.getGeometry()
        self.ui = loadUi(".\\resources\\interfaces\\getMultipleOffsets\\getMultipleOffsets.ui", self)
        self.setGeometry(x, y, width, height)

        self.back.pressed.connect(self.getOffset)
        self.howTo.pressed.connect(self.howToMultipleOffsets)
        self.Next.pressed.connect(self.multOffsetsAllDone)

        self.show()

    def multOffsetsAllDone(self):
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
                self.oldOffsets = []
                self.patches = []
                
                #Writing all offsets that were given from user
                file = io.open(".\\resources\\offsets\\offsets.txt", "w", encoding="utf-8")
                text = self.offsets.toPlainText()
                file.write(text)
                file.close()

                #Reading the offsets
                hexCheckOffset = True
                file = io.open(".\\resources\\offsets\\offsets.txt", "r", encoding="utf-8")
                for lines in file.readlines():
                    try:
                        tokens = lines.split(" ")
                        self.oldOffsets.append(tokens[0])

                        #Making sure patch is a valid hex number...
                        if tokens[0] != " ":
                            try:
                                int(tokens[0], 16)
                            except:
                                hexCheckOffset = False
                    except:
                        continue
                file.close()

                #Reading the patches
                hexCheckPatch = True
                file = io.open(".\\resources\\offsets\\offsets.txt", "r", encoding="utf-8")
                for lines in file.readlines():
                    try:
                        tokens = lines.split(" ")
                        self.patches.append(tokens[1])

                        #Making sure patch is a valid hex number...
                        if tokens[1] != " ":
                            try:
                                int(tokens[1], 16)
                            except:
                                hexCheckPatch = False
                    except:
                        continue
                file.close()

                #Making sure user has findBytes.py downloaded...
                self.findBytes("full")

                #Porting the offsets via findBytes.py
                self.ported = []
                for items in range(len(self.oldOffsets)):
                    try:
                        fixedOffset = self.oldOffsets[items].split("\n")
                        self.oldOffsets[items] = fixedOffset[0]
                        
                        cmd = str("python " + ".\\resources\\tools\\findBytes\\findBytes.py " + str(self.oldRemoveHeader) + " " + str(self.newRemoveHeader) + " " + str(self.oldOffsets[items]))
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
                    
                #Checking if number of offsets = number of patches
                if len(self.oldOffsets) != len(self.patches):
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Found empty lines...")
                    self.choice.setText('It looks like you have empty lines before, in the middle, or after your offsets. Please remove these unnecessary lines first, before proceeding.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                #Checking if user entered valid offsets/patches...
                elif hexCheckOffset == False and hexCheckPatch == False:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Invalid hex digits...")
                    self.choice.setText('One or more of your offsets and patches are invalid hex numbers. Please make sure you typed your offsets and patches in correctly, then try again.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                elif hexCheckOffset == False:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Invalid hex digits...")
                    self.choice.setText('One or more of your offsets is not a valid hex number. Please make sure you typed your offsets in correctly, then try again.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                elif hexCheckPatch == False:
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Invalid hex digits...")
                    self.choice.setText('One or more of your patches is not a valid hex number. Please make sure you typed your patches in correctly, then try again.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                else:
                    self.allDoneMultipleOffsets()

    def allDoneMultipleOffsets(self):
        x, y, width, height = self.getGeometry()
        self.ui = loadUi(".\\resources\\interfaces\\multAllDone\\multAllDone.ui", self)
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
                                             


    def allDone(self):
        """Last UI--returns your new offset via findBytes--"""
        #Making sure user has findBytes.py downloaded...
        self.findBytes("full")
        # Makes sure all info is filled out on-screen
        if str(self.offset.toPlainText()) == "":
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Warning)
            self.choice.setWindowTitle("Is everything filled out?")
            self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
            self.choice.setStandardButtons(QMessageBox.Ok)
            self.choice.exec_()

        else:
            #Checking if user entered valid offsets/patches...
            hexCheck = True
            try:
                int(self.offset.toPlainText(), 16)
            except:
                hexCheck = False
                
            #Telling user their offset is not a valid hex number (if it isn't)
            if hexCheck == False:
                self.choice = QMessageBox()
                self.choice.setIcon(QMessageBox.Warning)
                self.choice.setWindowTitle("Invalid hex digits...")
                self.choice.setText('Your patch is an invalid hex number. Please make sure you typed your offset in correctly, then try again.')
                self.choice.setStandardButtons(QMessageBox.Ok)
                self.choice.exec_()
            else:
                #Reading output from findBytes.py
                try:
                    cmd = str("python " + ".\\resources\\tools\\findBytes\\findBytes.py " + str(self.oldRemoveHeader) + " " + str(self.newRemoveHeader) + " " + str(self.offset.toPlainText()))
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)#, stderr=subprocess.IGNORE)
                    finalOutput = p.stdout.read()
                    retcode = p.wait()
                    finalOutput = str(finalOutput)
                    finalOutput = finalOutput[2:len(finalOutput) - 5]
                except:
                    pass
                ######

                x, y, width, height = self.getGeometry()
                self.ui = loadUi(".\\resources\\interfaces\\allDone\\allDone.ui", self)
                self.setGeometry(x, y, width, height)

                # Setting old offset and new, ported offset...
                self.newOffset.setPlainText(str(finalOutput))
                self.oldOffset.setPlainText(str(self.offset.toPlainText()))

                if str(finalOutput)[0] == "-":
                    self.choice = QMessageBox()
                    self.choice.setIcon(QMessageBox.Warning)
                    self.choice.setWindowTitle("Failed to port...")
                    self.choice.setText('Your offset could not be ported.')
                    self.choice.setStandardButtons(QMessageBox.Ok)
                    self.choice.exec_()
                ######

                self.sameFiles.pressed.connect(self.getOffset)
                self.differentFiles.pressed.connect(self.startOldFile)
                self.quit.pressed.connect(self.quitProgram)

                self.credits.pressed.connect(self.creditWin)
                self.convertOffset.pressed.connect(self.offsetConversions)

                self.show()

    #Functions that create Secondary Windows

    def newWindowNSO(self):
        self.window = decompressNSO()
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

        self.ui = loadUi(".\\resources\\interfaces\\decompressNSOInstructions\\decompressNSOInstructions.ui", self)

        self.show()

class offsetTut(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(offsetTut, self).__init__(*args, **kwargs)

        self.ui = loadUi(".\\resources\\interfaces\\offsetInstructions\\offsetInstructions.ui", self)

        self.show()

class credit(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(credit, self).__init__(*args, **kwargs)

        self.ui = loadUi(".\\resources\\interfaces\\credits\\credits.ui", self)

        self.show()

class convertOffset(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(convertOffset, self).__init__(*args, **kwargs)

        self.ui = loadUi(".\\resources\\interfaces\\convertOffset\\convertOffset.ui", self)

        self.show()

class multOffsetsHelp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(multOffsetsHelp, self).__init__(*args, **kwargs)

        self.ui = loadUi(".\\resources\\interfaces\\multipleOffsetsInstructions\\multipleOffsetsInstructions.ui", self)

        self.show()

class finalOptions(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(finalOptions, self).__init__(*args, **kwargs)

        self.arguments = args[0]

        self.ui = loadUi(".\\resources\\interfaces\\options\\options.ui", self)

        self.offsetConversions.pressed.connect(self.offsetCon)
        self.sameFiles.pressed.connect(self.getSameFilesOffset)
        self.differentFiles.pressed.connect(self.getDifferentFilesOffset)
        self.quit.pressed.connect(self.quitProgram)
        self.credits.pressed.connect(self.creditProgram)

        self.show()

    def offsetCon(self):
        self.window = convertOffset()
        self.window.show()

    def getSameFilesOffset(self):
        self.close()
        self.arguments.getOffset()

    def getDifferentFilesOffset(self):
        self.close()
        self.arguments.startOldFile()

    def quitProgram(self):
        sys.exit(0)

    def creditProgram(self):
        self.window = credit()
        self.window.show()


######################################################################################### 

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    app.exec_()
