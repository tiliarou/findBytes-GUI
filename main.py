""" This code was rushed in about 24 hours. Expect bugs, and poor coding; and probably some other 
stuff too that I can't think of currently ¯\_(ツ)_/¯ . Besides all of that though, I hope you find the tool useful. Cheers """

import PyQt5
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import *
import sys
import os
import time
from PyQt5 import QtCore 
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit

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
            counter = 0

        super(MainWindow, self).__init__(*args, **kwargs)

        #Getting screen size, to then load the UI at its center
        screen = app.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height()

        global halfWidth, halfHeight
        halfWidth = width/2
        halfHeight = height/2

        
        self.ui = loadUi(".\\resources\\interfaces\\startUp\\startUp.ui", self)
        self.setGeometry(0, 0, halfWidth, halfHeight)

        self.Start.pressed.connect(self.startOldFile)

        self.show()

        #Declaring variables, to prevent future possible errors, later on.
        self.oldFileDir = ""
        self.newFileDir = ""

        self.oldFileHeader = ""
        self.newFileHeader = ""

    def getGeometry(self):
        """Gets location of Window, so when user loads new UI, it stays there."""
        x = self.frameGeometry().x()
        y = self.frameGeometry().y()
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        return int(x), int(y), int(width), int(height)

    def startOldFile(self):
        """Loads the UI that asks for user's old file (the one they have the offset for)"""
        x, y, width, height = self.getGeometry()
        self.ui = loadUi(".\\resources\\interfaces\\oldFile\\oldFile.ui", self)
        self.setGeometry(x, y, width, height)

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

                self.here_2.pressed.connect(self.newWindowOffsetTut)
                self.Next_2.pressed.connect(self.allDone)

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

            self.here_2.pressed.connect(self.newWindowOffsetTut)
            self.Next_2.pressed.connect(self.allDone)

            self.oldFileSet.setText(str(self.oldFileDir) + "; " + self.oldFileHeader)
            self.newFileSet.setText(str(self.newFileDir) + "; " + self.newFileHeader)

            self.show()


    def allDone(self):
        """Last UI--returns your new offset via findBytes--"""
        # Makes sure all info is filled out on-screen
        if str(self.offset.toPlainText()) == "":
            self.choice = QMessageBox()
            self.choice.setIcon(QMessageBox.Warning)
            self.choice.setWindowTitle("Is everything filled out?")
            self.choice.setText('You are missing required information. Please fulfil these requirements first, before proceeding. When done, click "Next" again.')
            self.choice.setStandardButtons(QMessageBox.Ok)
            self.choice.exec_()

        else:
            os.system("python " + ".\\resources\\tools\\findBytes\\findBytes.py " + str(self.oldRemoveHeader) + " " + str(self.newRemoveHeader) + " " + str(self.offset.toPlainText()))

            x, y, width, height = self.getGeometry()
            self.ui = loadUi(".\\resources\\interfaces\\allDone\\allDone.ui", self)
            self.setGeometry(x, y, width, height)

            self.sameFiles.pressed.connect(self.getOffset)
            self.differentFiles.pressed.connect(self.__init__)
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
        self.window = credits()
        self.window.show()

    def offsetConversions(self):
        self.window = convertOffset()
        self.window.show()

    #############################################

    def quitProgram(self):
        """Quits program"""
        sys.exit()


# Secondary Windows [ex. The Button "here" creates one of these]

class decompressNSO(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(decompressNSO, self).__init__(*args, **kwargs)

        global halfWidth, haldHeight
        self.ui = loadUi(".\\resources\\interfaces\\decompressNSOInstructions\\decompressNSOInstructions.ui", self)
        self.setGeometry(0, 0, halfWidth, halfHeight)

        self.show()

class offsetTut(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(offsetTut, self).__init__(*args, **kwargs)

        global halfWidth, halfHeight
        self.ui = loadUi(".\\resources\\interfaces\\offsetInstructions\\offsetInstructions.ui", self)
        self.setGeometry(0, 0, halfWidth, halfHeight)

        self.show()

class credits(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(credits, self).__init__(*args, **kwargs)

        global halfWidth, halfHeight
        self.ui = loadUi(".\\resources\\interfaces\\credits\\credits.ui", self)
        self.setGeometry(0, 0, halfWidth, halfHeight)

        self.show()

class convertOffset(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(convertOffset, self).__init__(*args, **kwargs)

        global halfWidth, halfHeight
        self.ui = loadUi(".\\resources\\interfaces\\convertOffset\\convertOffset.ui", self)
        self.setGeometry(0, 0, halfWidth, halfHeight)

        self.show()


######################################################################################### 

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    app.exec_()
