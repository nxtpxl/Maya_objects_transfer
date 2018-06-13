
import os
import site
import Qt
from Qt import QtWidgets
import re
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance
import maya.cmds as cmds
import os, glob, time
import sys
import getpass
import maya.mel as mel

import os


class importExport(QWidget):

    def __init__(self):
        path = os.path.dirname(__file__) + '/cony_n_paste.ui'
        QWidget.__init__(self)
        self.userdataPath = 'L:/NXTPXLENT/pipe___RND/users'
        self.LocalUserName= getpass.getuser()
        self.local_user = os.path.join(self.userdataPath, self.LocalUserName, 'copyNpaste_data')

        self.ui = QUiLoader().load(path)
        self.localUserContentDirCheck()
        self.usersList()
        self.setUserName()
        self.selectUser()
        self.ui.files_tableWidget.verticalHeader().setVisible(False)
        self.ui.users_comboBox.currentIndexChanged.connect(self.selectUser)

        self.ui.files_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.files_tableWidget.customContextMenuRequested.connect(self.rightClickPopup)
        self.ui.files_tableWidget.clicked.connect(self.selectedFileName)

        self.ui.exportSelected_pushButton.clicked.connect(self.exportSelected)

        self.ui.files_tableWidget.resizeColumnsToContents()
        self.ui.users_comboBox.setStyleSheet('selection-background-color: rgb(0,168,0)')


        self.ui.files_tableWidget.setStyleSheet("QTableView { background-color: rgb(0, 0, 0)}")
        self.ui.files_tableWidget.setStyleSheet("QTableView {selection-background-color:rgb(0, 255, 0)}")
        self.ui.files_tableWidget.setStyleSheet("QTableView {selection-color:rgb(0, 0, 0)}")
        self.ui.files_tableWidget.setStyleSheet("QTableView {background-color:rgb(30, 30, 30)}")

        self.ui.files_tableWidget.setStyleSheet("""QTableView {
                                                    selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.8,
                                                                                stop: 0 green, stop: 1 black);
                                                }""")

        self.ui.float_on_top_checkBox.toggled.connect(self.AlwaysOn_top)
        self.ui.float_on_top_checkBox.setStyleSheet("color: grey")
        self.ui.groupBox_4.setStyleSheet("""QGroupBox { background-color: rgb(70, 70, 70)}
                                             QGroupBox { border: 1.2px solid green;}""")

        self.ui.groupBox_2.setStyleSheet("""QGroupBox { background-color: rgb(70, 70, 70)}
                                             QGroupBox { border: 1.2px solid green;}""")

        self.ui.groupBox.setStyleSheet("""QGroupBox { background-color: rgb(70, 70, 70)}
                                             QGroupBox { border: 1.2px solid green;}""")

        self.ui.files_tableWidget.setCornerButtonEnabled (True)
        self.ui.files_tableWidget.resizeColumnsToContents()
        self.ui.files_tableWidget.setColumnWidth(0,295)
        self.ui.files_tableWidget.setColumnWidth(1,100)

    def AlwaysOn_top(self):
        if self.ui.float_on_top_checkBox.isChecked():
            self.ui.setWindowFlags(self.ui.windowFlags() | Qt.WindowStaysOnTopHint)
            self.ui.float_on_top_checkBox.setStyleSheet("color: lightGreen")
            self.ui.show()
        else:
            self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.ui.float_on_top_checkBox.setStyleSheet("color: grey")
            self.ui.show()

    def rightClickPopup(self, point):
        menu = QMenu()

        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        menu.setFont(font1)
        menu = QMenu()
        menu.setStyleSheet("""QMenu {background-color: blue;}
                                  QMenu::item:selected {background-color: black}
                                  QMenu::separator {height: 1px;background: lightblue;margin-left: 10px;margin-right: 5px;}
                               """)
        menu.setFont(font1)
        menu.addSeparator()
        menuOption_1 = menu.addAction("Import selected File            ")
        menu.addSeparator()
        menuOption_2 = menu.addAction("Reference Selected File         ")

        if str(self.ui.users_comboBox.currentText()) == self.LocalUserName:
            menu.addSeparator()
            menuOption_3= menu.addAction("Rename Selected                  ")
            menu.addSeparator()
            menuOption_4= menu.addAction("Delete Selected                  ")
        else:
            pass
        action = menu.exec_(self.ui.files_tableWidget.mapToGlobal(point))
        clickedFileName = self.selectedFileName()
        filePath = (self.seletedFilePath()+'.ma')
        print (filePath)
        separator = os.path.normpath("/")
        path = re.sub(re.escape(separator), "/", filePath)
        print (path)
        if action == menuOption_1:
            print ('importing file')
            mel.eval(
                    'file -import -type "mayaAscii" -mergeNamespacesOnClash false -options "v=0;"  -pr  "%s"' % (
                    path))
        if action == menuOption_2:
            print ('refrencing file')
            mayaFile = path
            before = set(cmds.ls(type='transform'))
            cmds.file(mayaFile, reference=True)
            after = set(cmds.ls(type='transform'))
            imported = after - before
            print imported

        # if local user matched the selected than load else pass
        if str(self.ui.users_comboBox.currentText()) == self.LocalUserName:
            if action == menuOption_3:
                print ('rename file')
                notesUpdateUI = 'renameUI'
                text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'New name: ')
                if ok:
                    newFileName = str(text)
                    if newFileName == '':
                        cmds.confirmDialog(title="ERROR...", message="Not a valif file name.          ")
                    else:
                        selectedUser = str(self.ui.users_comboBox.currentText())
                        selectedFile = self.selectedFileName()
                        oldName = os.path.join(self.userdataPath,selectedUser, 'copyNpaste_data', selectedFile + ".ma" )
                        newName = os.path.join(self.userdataPath,selectedUser, 'copyNpaste_data', (newFileName + ".ma"))
                        os.rename(oldName, newName)
                        self.selectUser()
                else:
                    pass

            if action == menuOption_4:
                print ('delete file')
                os.remove(path)
                self.selectUser()
            else:
                pass

    def localUserContentDirCheck(self):
        lu =  os.path.join(self.userdataPath, self.LocalUserName)
        if os.path.isdir(lu) == True:
            pass
        else:
            os.mkdir(lu)

        localPath = os.path.join(self.userdataPath, self.LocalUserName, 'copyNpaste_data')
        if os.path.isdir(localPath) == True:
            pass
        else:
            os.mkdir(localPath)

    def exportSelected(self):
        newFileName = str(self.ui.newExportContentName.text())
        print (newFileName)

        if newFileName == '':
            cmds.confirmDialog(title="ERROR...",
                               message="Please enter a valid name for the content you want to save.          ")
        else:
            slObj = cmds.ls(sl=True)
            if slObj == []:
                cmds.confirmDialog(title="ERROR...", message="No Items are selected to save.          ")
            else:
                fileToSavePath = os.path.join(self.userdataPath,self.LocalUserName, 'copyNpaste_data', (newFileName + '.ma'))
                separator = os.path.normpath("/")
                if separator != "/":
                    path = re.sub(re.escape(separator), "/", fileToSavePath)
                    print (path)
                    mel.eval('file -force -options "v=0;" -typ "mayaAscii" -pr -es "%s"' % (path))
                    self.selectUser()
                    self.ui.newExportContentName.clear()

    def seletedFilePath(self):
        selectedUser = str(self.ui.users_comboBox.currentText())
        selectedFile = self.selectedFileName()
        filepath = os.path.join(self.userdataPath,selectedUser, 'copyNpaste_data', selectedFile )
        return filepath

    def selectedFileName(self):
         fileName = str(self.ui.files_tableWidget.currentItem().text())
         return fileName

    def usersList(self):
        existingUsers = sorted(os.listdir(self.userdataPath))
        users = []
        for d in existingUsers:
            x = os.path.join(self.userdataPath, d ,'copyNpaste_data')
            if os.path.isdir(x) == True:
                users.append(d)
            else:
                pass
        users = sorted(users)
        self.ui.users_comboBox.addItems(users)

    def setUserName(self):
        existingUsers = sorted(os.listdir(self.userdataPath))
        users = []
        for d in existingUsers:
            z = os.path.join(self.userdataPath, d, 'copyNpaste_data')
            if os.path.isdir(z) == True:
                users.append(d)
            else:
                pass
        users = sorted(users)
        self.ui.users_comboBox.setCurrentIndex(1)
        for val, user in enumerate(users, 0):

            if user == self.LocalUserName:
                self.ui.users_comboBox.setCurrentIndex(val)
                self.updateFilesList(str(self.LocalUserName))

                break
            else:
                self.ui.users_comboBox.setCurrentIndex(0)
    def updateFilesList(self, userName):
        p = os.path.join(self.userdataPath, userName, 'copyNpaste_data')
        existingFiles = sorted(os.listdir(p))

        tr=  os.path.join(self.userdataPath, userName, 'copyNpaste_data')
        search_dir = tr
        os.chdir(search_dir)
        files = filter(os.path.isfile, os.listdir(search_dir))
        files = [os.path.join(search_dir, f) for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        mayaFiles = []
        for f in files:
            fName = os.path.basename(f)
            mayaFiles.append(fName)
        return mayaFiles

    def selectUser(self):
        user_name = str(self.ui.users_comboBox.currentText())
        SelectedUserFilesList = self.updateFilesList( user_name)
        self.ui.files_tableWidget.clearContents()
        self.ui.files_tableWidget.setRowCount(len(SelectedUserFilesList))
        rowPosition = self.ui.files_tableWidget.rowCount()
        SelectedUserFilesList.reverse()

        if len(SelectedUserFilesList) == 0:
            pass
        else:
            for i, File in enumerate(SelectedUserFilesList, 0):
                self.ui.files_tableWidget.setItem(i, 0, QTableWidgetItem(File.rsplit('.', 1)[0]))
                filepath = os.path.join(self.userdataPath,user_name,'copyNpaste_data', File )
                modifiedTime =  time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(os.path.getmtime(filepath)))
                self.ui.files_tableWidget.setItem(i, 1, QTableWidgetItem(modifiedTime))


def runImport():
    global ImportUI
    ImportUI = importExport()
    ImportUI.ui.show()


runImport()
