#!/usr/bin/env python3
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui import selectprojDialog, newprojDialog, MainWindow, copyingFilesDialog, settingsDialog, projectSettingsDialog, GitHubPushDialog, LoginGitDialog, buildRpmWizard, rpmProgressDialog, importFromGitHubDialog

############IMPORTS#########
from cryptography.fernet import Fernet
import sys
from os import path as p
import shutil, os, configparser, glob, json, tarfile, time, pygit2, string, random
from pygit import pygit
from send2trash import send2trash
from subprocess import getoutput
from datetime import datetime
############################
import logging
logging.basicConfig()
from pyqode.qt import QtWidgets
from pyqode.python.backend import server
from pyqode.python.widgets import PyCodeEdit
from pyqode.python.widgets import code_edit
################################
from pyqode.core.api import TextHelper
from pyqode.qt import QtWidgets
from pyqode.python.widgets import PyInteractiveConsole, PyCodeEdit
################################
import sys
from pyqode.qt import QtWidgets
from pyqode.core.modes import CheckerMessage, CheckerMessages
from pyqode.core.widgets import ErrorsTable
################################

class selectProjectDialog(QDialog):
    def __init__(self):
        super(selectProjectDialog, self).__init__()
        self.ui = selectprojDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.pushButton_3.clicked.connect(self.openNewProjectDialog)
        self.ui.pushButton.clicked.connect(self.startProject)
        self.ui.listWidget.doubleClicked.connect(self.startProject)
        
        self.loadSettings()
        self.loadProjectsList()
        
    def startProject(self):
        for proj in list(glob.glob(Settings.workspace + "/*")):
            if not p.isfile(p.join(proj, ".BlackDevelop.conf")):
                continue
            currentItem = self.ui.listWidget.currentItem()
            
            conf = configparser.ConfigParser()
            conf.read(p.join(proj, ".BlackDevelop.conf"))
            if not currentItem.text() == conf["Info"]['name']:
                continue
            Settings.projectName = conf['Info']['Name']
            Settings.projectVersion = conf['Info']['version']
            Settings.projectPkg = conf['Info']['package']
            Settings.projectIcon = conf['Info']['icon']
            Settings.projectLanguage = conf['Info']['language']
            Settings.projectExec = conf['Info']['exec']
            Settings.projectPath = proj
            Settings.projectIconPath = p.join(Settings.projectPath, Settings.projectIcon)
            Settings.projectExecPath = p.join(Settings.projectPath, Settings.projectExec)
            Settings.projectConf = p.join(Settings.projectPath, ".BlackDevelop.conf")
            Settings.projectLastOpenedFiles = conf.get('Info', 'LastFiles')
            Settings.projectSrc = p.join(Settings.projectPath, "usr/src", Settings.projectPkg)
            Settings.loginGitHub = False
            Settings.GitHubRepo = False
            Settings.passwordGitHub = False
            if conf.has_option('Info', "GitHubRepo"):
                Settings.GitHubRepo = conf['Info']['GitHubRepo']
            
            self.hide()
            self.MainWindow = BlackDevelopWindow()
            self.MainWindow.show()
            self.close()
            
    def loadProjectsList(self):
        for file in list(glob.glob(Settings.workspace + "/*")):
            if not p.exists(p.join(file, ".BlackDevelop.conf")):
                continue
            conf = configparser.ConfigParser()
            conf.read(p.join(file, ".BlackDevelop.conf"))
            proj = QListWidgetItem()
            proj.setText(conf['Info']['name'])
            proj.setIcon(QIcon(p.join(Settings.workspace, p.basename(file), conf['Info']['icon'])))
            self.ui.listWidget.addItem(proj)
    
    def loadSettings(self):
        Settings.path = p.join(p.expanduser("~"), ".config/blackdevelop")
        Settings.file = p.join(Settings.path, "BlackDevelop.conf")
        if not p.isfile(Settings.file):
            self.createSettings()
        Settings.key = Fernet(b'JQZ_N16aWv81fei3AfB-1-9IPn2DE-Z11e_BtL3yLwg=')
        conf = configparser.ConfigParser()
        conf.read(Settings.file)
        Settings.workspace = conf['User']['workspace']
        if not p.isdir(Settings.workspace):
            dialog = QFileDialog()
            Settings.workspace = dialog.getExistingDirectory(None, 'Please select a new workspace', p.expanduser('~'), QFileDialog.ShowDirsOnly)
            if Settings.workspace == "":
                sys.exit()
            conf['User']['workspace'] = Settings.workspace
            with open(Settings.file, 'w') as configfile:
                configfile.truncate(0)
                conf.write(configfile)
    def createSettings(self):
        os.makedirs(Settings.path)
        conf = configparser.ConfigParser()
        conf.add_section('User')
        conf['User'] = {'workspace': p.join(p.expanduser('~'), ".BlackDevelop")}
        with open(Settings.file, 'w') as configfile:
            conf.write(configfile)
        if not p.exists(p.join(p.expanduser('~'), ".BlackDevelop")):
            os.makedirs(p.join(p.expanduser('~'), ".BlackDevelop"))
    def openNewProjectDialog(self):
        self.hide()
        self.dialog = newProjectDialog()
        self.dialog.exec_()
        self.show()
        self.ui.listWidget.clear()
        self.loadProjectsList()
        
        
class newProjectDialog(QWizard):
    def __init__(self):
        super(newProjectDialog, self).__init__()
        self.ui = newprojDialog.Ui_Wizard()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.iconSelect)
        self.button(QWizard.FinishButton).clicked.connect(self.buildProject)

    def buildProject(self):
        Settings.projectName = self.ui.lineEdit.text()
        shutil.copytree(p.join("blackdevelop-projects", self.ui.comboBox.currentText(), self.ui.comboBox_2.currentText()), p.join(Settings.workspace, Settings.projectName))
        Settings.projectPkg = Settings.projectName.lower().replace(" ", "-")
        Settings.projectPath = p.join(Settings.workspace, Settings.projectName)
        shutil.move(p.join(Settings.projectPath, "usr/src/myapp"), p.join(Settings.projectPath, "usr/src", Settings.projectPkg))
        shutil.move(p.join(Settings.projectPath, "usr/src", Settings.projectPkg, "myapp.py"), p.join(Settings.projectPath, "usr/src", Settings.projectPkg, self.ui.lineEdit.text() + ".py"))
        Settings.projectVersion = self.ui.lineEdit_2.text()
        Settings.projectIcon = self.ui.label_7.text()
        shutil.copy(Settings.projectIcon, p.join(Settings.projectPath, "usr/share/pixmaps", Settings.projectPkg + ".png"))
        Settings.projectIcon = p.join("usr/share/pixmaps", Settings.projectPkg + ".png")
        conf = configparser.ConfigParser()
        Settings.projectLanguage = "Python3-Qt5"
        Settings.projectExec = p.join("usr/src", Settings.projectPkg, Settings.projectName + ".py")
        conf["Info"] = {'Name': Settings.projectName,
                        'Version': Settings.projectVersion,
                        'Icon': Settings.projectIcon,
                        'Package': Settings.projectPkg,
                        'Language': Settings.projectLanguage,
                        'Exec': Settings.projectExec,
                        'LastFiles': '["' + p.join(Settings.projectPath, Settings.projectExec) + '"]'}
        Settings.projectConf = p.join(Settings.projectPath, ".BlackDevelop.conf")
        with open(Settings.projectConf, 'w') as configfile:
            conf.write(configfile)
    def iconSelect(self):
        options = QFileDialog.Options()
        self.icon, _ = QFileDialog.getOpenFileName(self,"Select program icon", p.expanduser('~'),"Icon files (*.png)", options=options)
        if not self.icon:
            return None
        self.ui.label_7.setText(self.icon)
        self.ui.pushButton.setIcon(QIcon(self.icon))

class Settings(object):
    def __init__(self):
        super(Settings, self).__init__()
        
class CopyThread(QThread):

    procDone = pyqtSignal(bool)
    procPartDone = pyqtSignal(int)

    def __init__(self, parent, source, destination):
        QThread.__init__(self, parent)
        self.source = source
        self.destination = destination

    def run(self):
        self.copy()
        self.procDone.emit(True)

    def copy(self):
        source_size = os.stat(self.source).st_size
        copied = 0
        source = open(self.source, "rb")
        target = open(self.destination, "wb")

        while True:
            chunk = source.read(1024)
            if not chunk:
                break
            target.write(chunk)
            copied += len(chunk)
            self.procPartDone.emit(copied * 100 / source_size)

        source.close()
        target.close()        

class SaveAsProjectDialog(QDialog):
    def __init__(self, destination):
        super(SaveAsProjectDialog, self).__init__()
        self.ui = copyingFilesDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        movie = QMovie("./gifs/copy-file.gif")
        self.ui.label_2.setMovie(movie)
        movie.start()
        
        self.ui.label.setText("Saving new project on disk ...")
        self.ui.progressBar.setMaximum(0)
        
        copy_thread = SaveThread(self, destination=destination)
        copy_thread.procDone.connect(self.close)
        copy_thread.start()

class SaveThread(QThread):
    procDone = pyqtSignal(bool)
    def __init__(self, parent, destination):
        QThread.__init__(self, parent)
        self.destination = destination
        
    def run(self):
        self.saveAs()
        self.procDone.emit(True)
    def saveAs(self):   
        tardir(Settings.projectPath, self.destination)
        
        
class CopyFilesDialog(QDialog):
    def __init__(self, source, destination):
        super(CopyFilesDialog, self).__init__()
        self.ui = copyingFilesDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        movie = QMovie("./gifs/copy-file.gif")
        self.ui.label_2.setMovie(movie)
        movie.start()
        
        copy_thread = CopyThread(self, source, destination)
        copy_thread.procPartDone.connect(self.update_progress)
        copy_thread.procDone.connect(self.close)
        copy_thread.start()
        
    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)


class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = settingsDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.loadSettings()
        self.ui.toolButton.clicked.connect(self.searchNewWorkspace)
        
    def accept(self):
        if p.isdir(self.ui.lineEdit.text()):
            Settings.workspace = self.ui.lineEdit.text()
            conf = configparser.ConfigParser()
            conf.add_section("User")
            conf['User'] = {'workspace': Settings.workspace}
            with open(Settings.file, 'w') as configfile:
                configfile.truncate(0)
                conf.write(configfile)
        super(SettingsDialog, self).accept()
        
    def searchNewWorkspace(self):
        dialog = QFileDialog()
        newpath = dialog.getExistingDirectory(self, "Select new workspace", )
        if newpath:
            self.ui.lineEdit.setText(newpath)
        
    def loadSettings(self):
        self.ui.lineEdit.setText(Settings.workspace)


class ProjectSettings(QDialog):
    def __init__(self):
        super(ProjectSettings, self).__init__()
        self.ui = projectSettingsDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.appIcon = Settings.projectIcon
        self.loadSettings()
        self.ui.pushButton.clicked.connect(self.openIcon)
        self.ui.toolButton.clicked.connect(self.openExec)
        
    def openExec(self):
        appExec, _ = QFileDialog.getOpenFileName(self,"Select program icon", p.join(Settings.projectPath, "usr/src", Settings.projectPkg),"All files (*.*")
        if not appExec or not p.isfile(appExec) or not Settings.projectPath in appExec:
            return None
        self.ui.lineEdit_5.setText(appExec)
        
    def openIcon(self):
        appIcon, _ = QFileDialog.getOpenFileName(self,"Select program icon", p.expanduser('~'),"Icon files (*.png)")
        if p.isfile(appIcon):
            self.appIcon = appIcon
            self.ui.pushButton.setIcon(QIcon(self.appIcon))
        
    def accept(self):
        if not p.isfile(self.appIcon) or not p.isfile(p.join(Settings.projectPath, self.ui.lineEdit_5.text())):
            super(ProjectSettings, self).accept()
        Settings.workspace = self.ui.lineEdit.text()
        conf = configparser.ConfigParser()
        if not self.appIcon == Settings.projectIcon:
            try:
                send2trash(p.join(Settings.projectPath, 'usr/share/pixmaps/', Settings.projectPkg + ".png"))
            except:
                print("W: Missing icon ...")
            Settings.projectIcon = "usr/share/pixmaps/" + Settings.projectPkg + ".png"
            Settings.projectIconPath = p.join(Settings.projectPath, Settings.projectIcon)
            shutil.copyfile(self.appIcon, p.join(Settings.projectPath, 'usr/share/pixmaps', Settings.projectPkg + ".png"))
            
        if not Settings.projectName == self.ui.lineEdit.text():
            Settings.projectName = self.ui.lineEdit.text()
            self.ui.lineEdit_6.setText(p.join(Settings.projectPath, "usr/src", Settings.projectName.replace(" ", "-").lower()))
            shutil.move(p.join(Settings.projectPath, "usr/src", Settings.projectPkg), p.join(Settings.projectPath, "usr/src", Settings.projectName.replace(" ", "-").lower()))
        Settings.projectVersion = self.ui.lineEdit_2.text()
        Settings.projectPkg = self.ui.lineEdit_6.text()
        Settings.projectExec = self.ui.lineEdit_5.text()
        Settings.projectExecPath = p.join(Settings.projectPath, Settings.projectExec)
        Settings.projectSrc = p.join(Settings.projectPath, "usr/src", Settings.projectPkg)
            
        conf["Info"] = {'Name': Settings.projectName,
                    'Version': Settings.projectVersion,
                    'Icon': Settings.projectIcon,
                    'Package': Settings.projectPkg,
                    'Language': Settings.projectLanguage,
                    'Exec': Settings.projectExec,
                    'LastFiles': '["' + p.join(Settings.projectPath, Settings.projectExec) + '"]'}
            
        with open(Settings.projectConf, 'w') as configfile:
            configfile.truncate(0)
            conf.write(configfile)

    def loadSettings(self):
        self.ui.lineEdit.setText(Settings.projectName)
        self.ui.lineEdit_2.setText(Settings.projectVersion)
        self.ui.pushButton.setIcon(QIcon(Settings.projectIconPath))
        self.ui.lineEdit_5.setText(Settings.projectExec)
        self.ui.lineEdit_6.setText(Settings.projectPkg)

class BuildSourceDialog(QDialog):
    def __init__(self, source, destination):
        super(BuildSourceDialog, self).__init__()
        self.ui = copyingFilesDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        movie = QMovie("./gifs/copy-file.gif")
        self.ui.label_2.setMovie(movie)
        movie.start()
        
        self.ui.label.setText("Exporting source to .tar.gz ...")
        self.ui.progressBar.setMaximum(0)
        
        build_thread = BuildThread(self, source, destination)
        build_thread.procDone.connect(self.accept)
        build_thread.start()

class BuildThread(QThread):
    procDone = pyqtSignal(bool)
    def __init__(self, parent, source, destination):
        QThread.__init__(self, parent)
        self.source = source
        self.destination = destination
        
    def run(self):
        self.build()
        self.procDone.emit(True)

    def build(self):
        tardir(path = self.source, tar_name = self.destination)
        
class LoginGitHubWindow(QDialog):
    def __init__(self):
        super(LoginGitHubWindow, self).__init__()
        self.ui = LoginGitDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.accepted.connect(self.saveLoginAndPassword)
        self.load()
        
    def load(self):

        if p.isfile(p.join(Settings.path, "user.github")) and p.isfile(p.join(Settings.path, "password.github")):
            with open(p.join(Settings.path, "user.github"), 'r') as file:
                user = file.read()
            login = Settings.key.decrypt(user.encode('utf-8')).decode('utf-8')
            
            with open(p.join(Settings.path, "password.github"), 'r') as file:
                password = file.read()
            passw = Settings.key.decrypt(password.encode('utf-8')).decode('utf-8')
            self.ui.lineEdit.setText(login)
            self.ui.lineEdit_2.setText(passw)

    def saveLoginAndPassword(self):
        passw = str(self.ui.lineEdit_2.text())
        login = str(self.ui.lineEdit.text())
        
        if not p.isfile(p.join(Settings.path, "user.github")) or p.join(Settings.path, "password.github"):
            open(p.join(Settings.path, "user.github"), 'a').close()
            open(p.join(Settings.path, "password.github"), 'a').close()

        Settings.passwordGitHub = passw
        Settings.loginGitHub = login
        
        passw = Settings.key.encrypt(passw.encode('utf-8'))
        login = Settings.key.encrypt(login.encode('utf-8'))
        
        with open(p.join(Settings.path, "user.github"), 'a') as file:
            file.write(login.decode())
        with open(p.join(Settings.path, "password.github"), 'a') as file:
            file.write(passw.decode())
            
class CommitGitHub(QDialog):
    def __init__(self):
        super(CommitGitHub, self).__init__()
        self.ui = GitHubPushDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        msgBox = QMessageBox( QMessageBox.Warning, "Please wait", "Preparing project for GitHub ...", QMessageBox.NoButton )

        l = msgBox.layout()
        l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()
        progress = QProgressBar()
        l.addWidget(progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )
        msgBox.show()
        
        self.pathFix()
        self.findCommits()

        self.ui.commandLinkButton_2.clicked.connect(self.commitFiles)
        self.ui.commandLinkButton.clicked.connect(self.pushFiles)
    
    def closeEvent(self, event):
        for newoldpath in Settings.newPaths:
            newpath = newoldpath[0]
            oldpath = newoldpath[1]
            file = newoldpath[2]
            
            if p.isdir(newpath):
                shutil.rmtree(newpath)
            elif p.isfile(newpath):
                os.remove(newpath)
                
            with open(p.join(file), 'r') as f :
                filedata = f.read()
            filedata = filedata.replace(newpath, oldpath)   
            with open(p.join(file), 'w') as f:
                f.write(filedata)
                
        event.accept() 
    
    def pushFiles(self):
        conf = configparser.ConfigParser()
        conf.read(Settings.projectConf)
        Settings.GitHubRepo = self.ui.lineEdit.text()
        if not Settings.GitHubRepo[-4:] == ".git":
            Settings.GitHubRepo = Settings.GitHubRepo + ".git"
        conf['Info']['GitHubRepo'] = Settings.GitHubRepo
        with open(Settings.projectConf, 'a') as file:
            file.truncate(0)
            conf.write(file)
            
        if not Settings.GitHubRepo[-4:] == ".git":
            Settings.GitHubRepo = Settings.GitHubRepo + ".git"
        if not Settings.loginGitHub or not Settings.passwordGitHub:
            self.dialog = LoginGitHubWindow()
            self.dialog.exec()
        self.hide()
        self.dialog = PushToGitProgressDialog()
        self.dialog.exec()
        
        for newoldpath in Settings.newPaths:
            newpath = newoldpath[0]
            oldpath = newoldpath[1]
            file = newoldpath[2]
            
            if p.isdir(newpath):
                shutil.rmtree(newpath)
            elif p.isfile(newpath):
                os.remove(newpath)
                
            with open(p.join(file), 'r') as f :
                filedata = f.read()
            filedata = filedata.replace(newpath, oldpath)
            with open(p.join(file), 'w') as f:
                f.write(filedata)
        
        
    def commitFiles(self):
        files = self.ui.listWidget.selectedItems()
        commitMessage = self.ui.lineEdit_3.text()
        for file in files:
            self.ui.listWidget.takeItem(self.ui.listWidget.row(file))
            self.ui.listWidget_2.addItem(file)
            file = file.text()
            file = file.replace(Settings.projectSrc + "/", "")
            os.system("git add '" + file + "'")
            os.system("git commit -m '" + commitMessage + "' '"+file+"'")
            
            
    def findCommits(self):
        os.chdir(Settings.projectSrc)

        os.system("git init .")

        
        newFiles = []
        changedFiles = []
        deletedFiles = []
        unstagedFiles = []
        
        if Settings.GitHubRepo:
            self.ui.lineEdit.setText(Settings.GitHubRepo)
        
        for line in getoutput("git status --porcelain .").splitlines():
            line = line.lstrip()
            mode, file_path = line.split(" ", 1)
            file_path = os.path.join(*file_path.split("/")[0:])
            file_path = file_path.replace('"', "").lstrip()     
            if mode == "D":
                deletedFiles.append(file_path)
                os.system("git rm --cached '"+ file_path + "'")
            if mode == "M":
                changedFiles.append(file_path)
            if mode == "A":
                newFiles.append(file_path)    
            os.system("git update-index --no-assume-unchanged '" + file_path + "'")
            
        for file in getoutput("git ls-files --others --exclude-standard .").splitlines():
            if p.isfile(p.join(Settings.projectSrc, file)):
                unstagedFiles.append(file)
        
        if not unstagedFiles == []:               
            for path in unstagedFiles:
                item = QListWidgetItem()
                item.setText(path.replace(Settings.projectSrc + "/", ""))
                brush = QBrush(QColor(138, 226, 52))
                brush.setStyle(Qt.SolidPattern)
                item.setBackground(brush)
                self.ui.listWidget.addItem(item)

        if not newFiles == []:               
            for path in newFiles:
                item = QListWidgetItem()
                item.setText(path.replace(Settings.projectSrc + "/", ""))
                brush = QBrush(QColor(138, 226, 52))
                brush.setStyle(Qt.SolidPattern)
                item.setBackground(brush)
                self.ui.listWidget_2.addItem(item)

        if not changedFiles == []: 
            for path in changedFiles:
                item = QListWidgetItem()
                item.setText(path.replace(Settings.projectSrc + "/", ""))
                brush = QBrush(QColor(252, 233, 79))
                brush.setStyle(Qt.SolidPattern)
                item.setBackground(brush)
                self.ui.listWidget.addItem(item)
                
        if not deletedFiles == []: 
            for path in deletedFiles:
                item = QListWidgetItem()
                item.setText(path.replace(Settings.projectSrc + "/", ""))
                brush = QBrush(QColor(239, 41, 41))
                brush.setStyle(Qt.SolidPattern)
                item.setBackground(brush)
                self.ui.listWidget.addItem(item)    

    def pathFix(self):
        Settings.newPaths = []
        for root, dirs, files in os.walk(Settings.projectPath):
            for file in files:
                file = p.join(root, file)
                filedata = ''
                if p.isdir(file):
                    continue
                try:
                    with open(p.join(root, file), 'r') as f :
                        filedata = f.read()
                except:
                    continue
                paths = filedata.split('"')
                if not len(paths) == 1:
                    newfile = ""
                    
                    for data in paths:
                        
                        if p.exists(p.join(Settings.projectPath, data)) and Settings.projectSrc in p.join(Settings.projectPath, data) and not data == '' and not data[:2] == './' and data[-4:] == ".png":         
                            filedata = filedata.replace('"' + data + '"', '"./pixmaps/' + p.basename(data) + '"')
                            Settings.newPaths.append(["./pixmaps/" + p.basename(data), data, file])
                        elif p.exists(p.join(Settings.projectPath, data)) and not Settings.projectSrc in p.join(Settings.projectPath, data) and not data == '' and not data[:2] == './':
                            newpath = p.join(Settings.projectSrc, data)
                            oldpath = p.join(Settings.projectPath, data)
                            if p.isfile(oldpath) and not p.isfile(newpath):
                                if not p.isdir(p.dirname(newpath)):
                                    os.makedirs(p.dirname(newpath))
                                if not p.isfile(newpath):
                                    shutil.copyfile(oldpath, newpath)
                                Settings.newPaths.append(["./" + data, data, file])
                                filedata = filedata.replace('"' + data + '"', '"./' + data + '"')
                            elif p.isdir(oldpath) and not p.isdir(newpath):
                                os.makedirs(newpath)
                                try:
                                    shutil.copytree(oldpath, newpath)
                                    Settings.newPaths.append(["./" + data, data, file])
                                except:
                                    print("W: Directory empty ...")
                                    Settings.newPaths.append(["./" + data, data, file])
                                filedata = filedata.replace('"' + data + '"', '"./' + data + '"')
                        elif p.exists(p.join(Settings.projectPath, data)) and Settings.projectSrc in p.join(Settings.projectPath, data) and not data == '' and not data[:2] == './':
                            newpath = p.join(Settings.projectSrc, data)
                            oldpath = p.join(Settings.projectPath, data)
                            if p.isfile(oldpath) and not p.isfile(newpath):
                                Settings.newPaths.append(["./" + data, data, file])
                            elif p.isdir(oldpath) and not p.isdir(newpath):
                                os.makedirs(newpath)
                                Settings.newPaths.append(["./" + data, data, file])
                            filedata = filedata.replace('"' + data + '"', '"./' + data + '"')
                    if file[-3:] == '.py' and not filedata == '':
                        with open(p.join(root, file), 'w') as f:
                            f.write(filedata)
        
                
class PushToGitProgressDialog(QDialog):
    def __init__(self):
        super(PushToGitProgressDialog, self).__init__()
        
        self.ui = copyingFilesDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        movie = QMovie("./gifs/copy-file.gif")
        self.ui.label_2.setMovie(movie)
        movie.start()
        
        self.ui.label.setText("Uploading to GitHub ...")
        self.ui.progressBar.setMaximum(0)
        
        send_to_git_thread = SendToGitThread(self)
        send_to_git_thread.procDone.connect(self.close)
        send_to_git_thread.procError.connect(self.error)
        send_to_git_thread.start()
        
    
    def error(self):
        self.close()
        print("E: Git-Push error ...")
        error_dialog = QErrorMessage()
        error_dialog.showMessage('Bad password, login, URL adress or too many connections today ...')
        error_dialog.exec()
        
class TimerThread(QThread):
    signal = pyqtSignal()
    def __init__(self, parent, time):
        QThread.__init__(self, parent)
        self.time = time
        
    def run(self):
        self.timer()

    def timer(self):
        while 1:
            time.sleep(self.time)
            self.signal.emit()
        

class SendToGitThread(QThread):
    procDone = pyqtSignal(bool)
    procError = pyqtSignal(bool)
    def __init__(self, parent):
        QThread.__init__(self, parent)
        
    def run(self):
        if self.push():
            self.procDone.emit(True)
        else:
            self.procError.emit(True)
    def push(self):
        try:
            local = pygit2.Repository(path=Settings.projectSrc)
            cred = pygit2.UserPass(username=Settings.loginGitHub, password=Settings.passwordGitHub)
            callbacks = pygit2.RemoteCallbacks(credentials=cred)
            try:
                remote = pygit2.remote.RemoteCollection(local)
                remote.delete('origin')
            except:
                print('I: Creating remote origin ...')
            
            local.create_remote('origin', Settings.GitHubRepo)
            remote = local.remotes['origin']
            remote.push(callbacks=callbacks, specs=['refs/heads/master:refs/heads/master'])
            return True
        except:
            return False
                    
                            
class ImportFromTgz(QDialog):
    def __init__(self, destination):
        super(ImportFromTgz, self).__init__()
        
        self.ui = copyingFilesDialog()
        self.ui.setupUi(self)
        
        self.ui.label.setText("Importing '"+self.desc+"' ...")
        self.ui.progressBar.setMaximum(0)
        
        copy_thread = ImportFromTgzThread(self, destination=destination)
        copy_thread.procDone.connect(self.close)
        copy_thread.start()

class ImportFromTgzThread(QThread):
    procDone = pyqtSignal(bool)
    def __init__(self, parent, destination):
        QThread.__init__(self, parent)
        self.destination = destination
        
    def run(self):
        self.script
        self.procDone.emit(True)
    
    def script(self):
        rand = "BlackDevUnpack-" + random(10)
        tmp = p.join("/usr/tmp", rand)
        os.makedirs(tmp)
        extract(self.destination, tmp)
        if not p.isfile(p.join(tmp,".BlackDevelop.conf")):
            print("E: File is not valid BlackDevelop project ...")
        else:
            shutil.move(tmp, Settings.workspace)
            print("BlackDev: Imported.")
        

class ImportFromGitHub(QDialog):
    def __init__(self):
        super(ImportFromGitHub, self).__init__()
        
        self.ui = importFromGitHubDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.toolButton.clicked.connect(self.selectIcon)
        
    def selectIcon(self):
        dialog = QFileDialog()
        iconpth, _ = dialog.getOpenFileName(self, 'Select program icon ...', p.expanduser('~'), 'Image files (*.png)')
        if not iconpth:
            return None
        self.ui.lineEdit_3.setText(iconpth)
    
    def accept(self):
        
        repo = self.ui.lineEdit.text()
        appname = self.ui.lineEdit_2.text()
        appver = self.ui.lineEdit_4.text()
        iconpth = self.ui.lineEdit_3.text()
        
        rand = "BlackDevUnpack-" + randomString(10)
        tmp = p.join("/usr/tmp", rand)
        os.makedirs(tmp)
        self.tmp = tmp
        
        self.close()
        self.dialog = progressFromGitHubDialog(appname, repo, appver, iconpth, tmp)
        self.dialog.exec()
        
        
        
class progressFromGitHubDialog(QDialog):
    def __init__(self, appname, repo, appver, iconpth, tmp):
        super(progressFromGitHubDialog, self).__init__()
        self.ui = copyingFilesDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.appname = appname
        self.tmp = tmp
        
        copy_thread = ImportFromGitHubThread(self, appname, repo, appver, iconpth, tmp)
        copy_thread.procDone.connect(self.setExec)
        copy_thread.start()
    
    def setExec(self):
        dialog = QFileDialog()
        projectExec, _ = dialog.getOpenFileName(self, 'Select program executable ...', p.join(Settings.workspace, p.basename(self.tmp), "usr/src/", self.appname.replace(" ","").lower()), 'All files (*.*)')
        if not projectExec:
            return None
        conf = configparser.ConfigParser()
        conf.read(p.join(Settings.workspace, p.basename(self.tmp), ".BlackDevelop.conf"))
        conf['Info']['Exec'] = projectExec.replace(p.join(Settings.workspace, p.basename(self.tmp)) + '/', "")
        with open(p.join(Settings.workspace, p.basename(self.tmp), ".BlackDevelop.conf"), 'a') as f:
            f.truncate(0)
            conf.write(f)
        self.close()
        

class ImportFromGitHubThread(QThread):
    procDone = pyqtSignal(bool)
    def __init__(self, parent, appname, repo, appver, iconpth, tmp):
        QThread.__init__(self, parent)
        self.appname = appname
        self.repo = repo
        self.appver = appver
        self.iconpth = iconpth
        self.tmp = tmp
        
    def run(self):
        self.script(self.appname, self.repo, self.appver, self.iconpth, self.tmp)
        self.procDone.emit(True)
        
    def script(self, appname, repo, appver, iconpth, tmp):
        
        print("BlackDev: Preparing directories ...")
        pkgname = appname.replace(" ","-").lower()
        os.makedirs(p.join(tmp, "usr/src"))
        os.makedirs(p.join(tmp, "usr/share/pixmaps"))
        shutil.copyfile(iconpth, p.join(tmp, "usr/share/pixmaps", pkgname + ".png"))
        
        print("BlackDev: Preparing configuration ...")
        conf = configparser.ConfigParser()
        conf.add_section('Info')
        if not repo[-4:] == ".git":
            repo = repo + ".git"
        conf["Info"] = {'Name': appname,
                        'Version': appver,
                        'Icon': "usr/share/pixmaps/"+pkgname+".png",
                        'Package': pkgname,
                        'Language': Settings.projectLanguage,
                        'LastFiles': '[]',
                        'githubrepo': repo}
        with open(p.join(tmp, ".BlackDevelop.conf"), 'a') as f:
            f.truncate(0)
            conf.write(f)
        os.chdir(p.join(tmp, 'usr/src'))

        print("BlackDev: Cloning from: '" +repo+"' ...")
        os.system("git clone '"+repo+"' > /dev/null")
        print("BlackDev: Importing project ...")
        shutil.move(tmp, Settings.workspace)
        for path in glob.glob(p.join(Settings.workspace, p.basename(self.tmp), 'usr/src/*')):
            shutil.move(path, p.join(Settings.workspace, p.basename(self.tmp), 'usr/src', p.basename(path).replace(" ", "").lower()))
        print("BlackDev: '"+appname+"' imported ...")


class BlackDevelopWindow(QMainWindow):
    def __init__(self):
        super(BlackDevelopWindow, self).__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(self.ui.actionNew_2)
        toolbar.addAction(self.ui.actionOpen)
        toolbar.addAction(self.ui.actionSave)
        toolbar.addSeparator()
        toolbar.addAction(self.ui.actionPackage)
        toolbar.addAction(self.ui.actionModule)
        toolbar.addAction(self.ui.actionImport)
        toolbar.addSeparator()
        toolbar.addAction(self.ui.actionRun_program)
        toolbar.addAction(self.ui.actionBuild)
        toolbar.addAction(self.ui.actionGitHub)
        
        self.ui.actionGitHub.setIcon(QIcon("ui/icons/x-github.png"))
        
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.ui.actionAll_files.triggered.connect(self.viewFiles)
        self.viewFiles()
        self.ui.actionModule.triggered.connect(self.addModule)
        self.ui.actionPackage.triggered.connect(self.addPackage)
        
        self.ui.actionMainWindow.triggered.connect(self.addUiMainWindow)
        self.ui.actionDialog.triggered.connect(self.addUiDialog)
        self.ui.actionWizard.triggered.connect(self.addUiWizard)

        self.ui.actionSource_directory.triggered.connect(self.newDir)
        self.ui.actionText_document.triggered.connect(self.newPlainFile)
        self.ui.actionBash_script.triggered.connect(self.newBashFile)
        self.ui.actionDelete.triggered.connect(self.deleteFile)
        self.ui.actionImport.triggered.connect(self.importFile)
        self.ui.actionRename.triggered.connect(self.renameFile)
        self.ui.actionBlackDevelop_settings.triggered.connect(self.blackDevelopSettings)
        self.ui.actionProject_settings.triggered.connect(self.projectSettings)
        self.ui.actionBuild_tar_gz_source.triggered.connect(self.exportSourceTgz)
        self.ui.actionGitHub.triggered.connect(self.exportToGitHub)
        self.logWidget = PyInteractiveConsole()
        self.ui.gridLayout_2.addWidget(self.logWidget, 0, 0, 1, 1)
        
        self.ui.dockWidget_2.setVisible(False)
        
        self.errorsTable = ErrorsTable()
        self.ui.gridLayout_4.addWidget(self.errorsTable, 0, 0, 1, 1)
        
        os.chdir(Settings.projectSrc)
        
        self.loadLastOpenedFiles()
        
        self.ui.actionRun_program.triggered.connect(self.runProject)
        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.ui.treeView.doubleClicked.connect(self.openFile)
        self.ui.actionSave.triggered.connect(self.saveAll)
        self.ui.actionBuild.triggered.connect(self.buildApp)
        self.ui.actionBuild_and_run.triggered.connect(self.buildAndRun)
        self.ui.actionSave_as.triggered.connect(self.saveAs)
        self.ui.actionFrom_tgz.triggered.connect(self.importFromTgz)
        self.ui.actionFrom_GitHub.triggered.connect(self.importFromGitHub)
        self.ui.actionClose.triggered.connect(self.closeProject)
        self.ui.actionNew_2.triggered.connect(self.newProject)
        self.ui.actionOpen.triggered.connect(self.openProject)
        self.ui.actionBuild_RPM_package.triggered.connect(self.buildRPM)
    
    def buildRPM(self):
        self.wizard = BuildRpm()
        self.wizard.exec()
        for arch in glob.glob(p.join(p.expanduser('~'), 'rpmbuild/RPMS/*')):
            for rpm in glob.glob(p.join(p.expanduser('~'), 'rpmbuild/RPMS', arch, '*.rpm')):
                dialog = QFileDialog()
                destination, _ = dialog.getSaveFileName(self, 'Save RPM file', p.expanduser('~'), "RPM packages (*.rpm)")
                shutil.move(rpm, destination)
                shutil.rmtree(p.join(p.expanduser('~'), 'rpmbuild'))
        self.pathFix()
    def closeProject(self):
        self.close()
        self.dialog = selectProjectDialog()
        self.dialog.show()
    
    def importFromGitHub(self):
        self.dialog = ImportFromGitHub()
        self.dialog.exec()
        self.buildApp()
    
    def importFromTgz(self):
        dialog = QFileDialog()
        path = dialog.getOpenFileName(self, 'Import from source', p.expanduser('~'), 'Tarball sources (*.tar.gz)')
        if not path:
            return None
        
        self.dialog = ImportFromTgz(path)
        self.dialog.show()
        
    def saveAs(self):
        dialog = QFileDialog()
        path, _ = dialog.getSaveFileName(self, 'Save as ...', p.expanduser('~'), "BlackDevelop project files (*.bdp)")
        if not path:
            return None
        self.dialog = SaveAsProjectDialog(path)
        self.show()
        
    def openProject(self):
        self.saveAll()
        self.close()
        self.dialog = selectProjectDialog()
        self.dialog.show()
        
    def newProject(self):
        self.saveAll()
        self.close()
        self.dialog = newProjectDialog()
        self.dialog.show()
    
    def buildAndRun(self):
        print("BlackDev: Building ...")
        self.buildApp()
        print("BlackDev: Running ...")
        self.runProject()
    
    def buildApp(self):
        for file in glob.glob(p.join(Settings.projectSrc, "ui/*.ui")):
            print("[pyuic5]: Compiling '"+p.basename(file)+"' ...")
            os.system("pyuic5 '" + file + "' -o '" + file.replace(".ui", ".py") + "'")
    def saveAll(self):
        for index in range(self.ui.tabWidget.count()):
            file, editor = self.getFileFromIndex(index)
            editor.file.save(file)
            
    def loadLastOpenedFiles(self):
        conf = configparser.ConfigParser()
        conf.read(Settings.projectConf)
        s = conf.get("Info","lastfiles")
        s = s.replace("'", '"')
        s = json.loads(s)
        for file in s:
            self.loadFile(file)
    
    def openFile(self):
        file = self.getPath()
        if file[-3:] == ".py":
            self.loadFile(file)
        else:
            os.system("xdg-open '"+file+"' &")    
    
    def closeTab(self, index):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setText("Save file?")
        box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Abort | QMessageBox.Save)
        box.setDefaultButton(QMessageBox.Save)
        box.exec_()
        clicked = box.clickedButton()
        clicked = clicked.text()

        if clicked == "Abort":
            self.ui.tabWidget.removeTab(index)
            self.updateFilesOpened()
        if clicked == "Cancel":
            return None
        if clicked == "Save":
            file, editor = self.getFileFromIndex(index)
            print("BlackDev: Saving '"+file+"' ...")
            editor.file.save(file)
            self.ui.tabWidget.removeTab(index)
            self.updateFilesOpened()
    
    def pathFix(self):
        os.chdir(Settings.projectPath)
        for root, dirs, files in os.walk(Settings.projectPath):
            for file in files:
                file = p.join(root, file)
                filedata = ''
                if p.isdir(file):
                    continue
                try:
                    with open(p.join(root, file), 'r') as f :
                        filedata = f.read()
                except:
                    continue
                paths = filedata.split('"')
                if not len(paths) == 1:
                    newfile = ""
                    
                    for data in paths:
                        
                        if p.exists(p.join(Settings.projectSrc, data[2:])) and data[:2] == "./":
                            newfile = data[2:]
                            filedata = filedata.replace(data, newfile)
                            fileInSrc = p.join(Settings.projectSrc, data[2:])
                            fileInPath = p.join(Settings.projectPath, data[2:])
                            if p.isfile(fileInSrc) and p.isfile(fileInPath):
                                os.remove(fileInSrc)
                            elif p.isdir(fileInSrc) and p.isdir(fileInPath):
                                try:
                                    shutil.rmtree()
                                except:
                                    print('I: Deleted empty directory ...')
                            elif p.isfile(fileInSrc) and not p.isfile(fileInPath):
                                shutil.move(fileInSrc, fileInPath)
                            elif p.isdir(fileInSrc) and not p.isdir(fileInPath):
                                shutil.move(fileInSrc, fileInPath)
                                
                        elif p.exists(data) and data[-4:] == '.png' and not Settings.projectPath in p.normpath(data):
                            pixmaps = p.join(Settings.projectSrc, 'pixmaps')
                            if not p.isdir(pixmaps):
                                os.makedirs(pixmaps)
                                
                            pixmap = p.join(pixmaps, p.basename(p.normpath(data)))
                            if not p.isfile(pixmap):
                                shutil.copy2(p.normpath(data), pixmaps)
                            pixmap = pixmap.replace(Settings.projectPath + "/", "")
                            filedata = filedata.replace(data, pixmap)
                        #elif p.exists(p.join(Settings.projectSrc, data[2:])) and data[:2] == "./":
                        #    oldpath = p.join(Settings.projectSrc, data[2:])
                        #    newpath = p.join(oldpath.replace(Settings.projectPath + "/", ""))
                        #    filedata = filedata.replace(data, newpath)
                        elif p.exists(data) and file[-3:] == '.py' and Settings.projectPath in p.normpath(data):
                            newfile = p.abspath(data)
                            newfile = newfile.replace(Settings.projectPath + "/", "")
                            filedata = filedata.replace(data, newfile)
                        
                    if file[-3:] == '.py' and not filedata == '':
                        with open(p.join(root, file), 'w') as f:
                            f.write(filedata)
                        
                            
    def runProject(self):
        self.saveAll()
        self.pathFix()     
        os.chdir(Settings.projectPath)
        self.logWidget.start_process(sys.executable, [p.join(Settings.projectPath, Settings.projectExec)])
        
    def loadFile(self, file):
        self.editor = PyCodeEdit(server_script=server.__file__)
        self.tab = QWidget()
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.addWidget(self.editor, 0, 0, 1, 1)
        self.ui.tabWidget.addTab(self.tab, file.replace(Settings.projectSrc + "/", ''))
        self.editor.file.open(file)
        self.updateFilesOpened()
        
    def getFileFromIndex(self, index):
        self.ui.tabWidget.setCurrentIndex(index)
        file = self.ui.tabWidget.tabText(index)
        tab = self.ui.tabWidget.currentWidget()
        _, editor = tab.children()
        file = p.join(Settings.projectSrc, file)
        return file, editor
    
    def updateFilesOpened(self):
        filesOpened = []
        for index in range(self.ui.tabWidget.count()):
            file, _ = self.getFileFromIndex(index)
            filesOpened.append(file)
        conf = configparser.ConfigParser()
        conf.read(Settings.projectConf)
        conf['Info']['lastfiles'] = str(filesOpened)
        with open(Settings.projectConf, 'a') as f:
            f.truncate(0)
            conf.write(f)
        
    def exportToGitHub(self):
        self.dialog = CommitGitHub()
        self.dialog.exec()
        self.buildApp()
        self.pathFix()
        
        
    def exportSourceTgz(self):
        dialog = QFileDialog()
        destination, _ = dialog.getSaveFileName(self, 'Export project to .tar.gz ...', p.expanduser('~'), "Tarball sources (*.tar.gz)")
        self.dialog = BuildSourceDialog(p.join(Settings.projectPath, "usr/src", Settings.projectPkg), destination + ".tar.gz")
        self.dialog.accepted.connect(self.show)
        self.dialog.show()
        self.hide()
        
    def projectSettings(self):
        self.dialog = ProjectSettings()
        self.dialog.show()
    def openNewProjectDialog(self):
        self.dialog = selectProjectDialog()
        self.dialog.show()
        self.close()
        
    def blackDevelopSettings(self):
        self.dialog = SettingsDialog()
        self.dialog.show()
        self.dialog.accepted.connect(self.openNewProjectDialog)
    
    def importFile(self):
        dialog = QFileDialog()
        destination = self.getPath()
        source, _ = dialog.getOpenFileName(self, 'Import file to: ' + p.basename(destination), p.expanduser('~'))
        if source:
            if p.isdir(destination):
                destination = p.join(destination, p.basename(source))
            else:
                destination = p.join(p.dirname(destination), p.basename(source))

            self.dialog = CopyFilesDialog(source, destination)
            self.dialog.show()

    def deleteFile(self):
        path = self.getPath()
        qm = QMessageBox()
        ret = qm.question(self,'', "Are you sure to move "+p.basename(path)+" to trash?", qm.Yes | qm.No)

        if ret == qm.Yes:
            try:
                send2trash(path)
            except:
                os.remove(path)
    
    def renameFile(self):
        path = self.getPath()
        i, okPressed = QInputDialog.getText(self, "Rename file (" + path + ")","New file/directory name ("+p.basename(path)+"):")
        if okPressed:
            os.rename(path, p.join(p.dirname(path), i))
        
    def newBashFile(self):
        i, okPressed = QInputDialog.getText(self, "Create new bash script (" + Settings.projectLanguage + ")","Bash script name:")
        if okPressed:
            path = self.getPath()
            if p.isfile(path):
                path = p.dirname(path)
            if not i[-3:] == ".sh":
                i = i + ".sh"
            open(p.join(path, i), 'a').close()

    def newPlainFile(self):
        i, okPressed = QInputDialog.getText(self, "Create new file (" + Settings.projectLanguage + ")","File name:")
        if okPressed:
            path = self.getPath()
            if p.isfile(path):
                path = p.dirname(path)
            open(p.join(path, i), 'a').close()

    def newDir(self):
        i, okPressed = QInputDialog.getText(self, "Create new source directory (" + Settings.projectLanguage + ")","Directory name:")
        if okPressed:
            path = self.getPath()
            if p.isfile(path):
                path = p.dirname(path)
            os.makedirs(p.join(path, i))

    def addUiWizard(self):
        i, okPressed = QInputDialog.getText(self, "Create new program window (" + Settings.projectLanguage + ")","Window (wizard) name:")
        if okPressed:
            if not i[-3:] == ".py":
                i = i + ".py"
            i = p.join(Settings.projectPath, "usr/src", Settings.projectPkg, "ui", i)
            shutil.copyfile(p.join("/usr/src/blackdevelop-projects/Python3/window_examples", "Wizard/Wizard.py"), i)
            shutil.copyfile(p.join("/usr/src/blackdevelop-projects/Python3/window_examples", "Wizard/Wizard.ui"), i.replace(".py", ".ui"))

    def addUiDialog(self):
        i, okPressed = QInputDialog.getText(self, "Create new program window (" + Settings.projectLanguage + ")","Window (dialog) name:")
        if okPressed:
            if not i[-3:] == ".py":
                i = i + ".py"
            i = p.join(Settings.projectPath, "usr/src", Settings.projectPkg, "ui", i)
            shutil.copyfile(p.join("/usr/src/blackdevelop-projects/Python3/window_examples", "Dialog/Dialog.py"), i)
            shutil.copyfile(p.join("/usr/src/blackdevelop-projects/Python3/window_examples", "Dialog/Dialog.ui"), i.replace(".py", ".ui"))
    
    def addUiMainWindow(self):
        i, okPressed = QInputDialog.getText(self, "Create new program window (" + Settings.projectLanguage + ")","Window (main) name:")
        if okPressed:
            if not i[-3:] == ".py":
                i = i + ".py"
            i = p.join(Settings.projectPath, "usr/src", Settings.projectPkg, "ui", i)
            shutil.copyfile(p.join("/usr/src/blackdevelop-projects/Python3/window_examples", "MainWindow/MainWindow.py"), i)
            shutil.copyfile(p.join("/usr/src/blackdevelop-projects/Python3/window_examples", "MainWindow/MainWindow.ui"), i.replace(".py", ".ui"))
    def getPath(self):
        index = self.ui.treeView.currentIndex()
        model = self.ui.treeView.model()
        path = model.filePath(index)
        if path == "":
            path = Settings.projectPath 
        return path  
    
    def addPackage(self):
        i, okPressed = QInputDialog.getText(self, "Create program package (" + Settings.projectLanguage + ")","Package name:")
        if okPressed:
            path = self.getPath()
            if p.isfile(path):
                path = p.dirname(path)
            os.makedirs(p.join(path, i))
            open(p.join(p.join(path, i), "__init__.py"), 'a').close()
    
    def addModule(self):
        i, okPressed = QInputDialog.getText(self, "Create program module (" + Settings.projectLanguage + ")","Module name:")
        if okPressed:
            path = self.getPath()
            if p.isfile(path):
                path = p.dirname(path)
            if not i[-3:] == ".py":
                i = i + ".py"
            open(p.join(path, i), 'a').close()
          
    def viewFiles(self):
        self.model = QFileSystemModel()
        if self.ui.actionAll_files.isChecked():
            self.ui.treeView.setModel(self.model)
            self.model.setRootPath(QDir.rootPath())
            self.ui.treeView.setRootIndex(self.model.index(Settings.projectPath))
            self.ui.treeView.setModel(self.model)
        else:
            self.ui.treeView.setModel(self.model)
            self.model.setRootPath(QDir.rootPath())
            self.ui.treeView.setRootIndex(self.model.index(p.join(Settings.projectPath, "usr/src", Settings.projectPkg)))
            self.ui.treeView.setModel(self.model)
          
class BuildRpm(QWizard):
    def __init__(self):
        super(BuildRpm, self).__init__()
        self.ui = buildRpmWizard.Ui_Wizard()
        self.ui.setupUi(self)
        self.loadUi()
        self.ui.lineEdit.textChanged.connect(self.setPkgName)
        self.ui.commandLinkButton.clicked.connect(self.addPkg)
        self.ui.commandLinkButton_2.clicked.connect(self.removePkg)
        
        self.ui.pushButton.clicked.connect(self.addToList1)
        self.ui.pushButton_3.clicked.connect(self.addToList2)
        self.ui.pushButton_5.clicked.connect(self.addToList3)
        self.ui.pushButton_2.clicked.connect(self.removeFromList1)
        self.ui.pushButton_4.clicked.connect(self.removeFromList2)
        self.ui.pushButton_6.clicked.connect(self.removeFromList3)
        
    
    def accept(self):
        self.close()
        self.progressDialog = RpmBuildProgressDialog(self.ui)
        self.progressDialog.exec()
        
    def removeFromList1(self):
        item = self.ui.listWidget.currentItem()
        self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
    def removeFromList2(self):
        item = self.ui.listWidget_2.currentItem()
        self.ui.listWidget_2.takeItem(self.ui.listWidget_2.row(item))
    def removeFromList3(self):
        item = self.ui.listWidget_3.currentItem()
        self.ui.listWidget_3.takeItem(self.ui.listWidget_3.row(item))
        
    def addToList1(self):
        item = QListWidgetItem()
        item.setText(self.ui.lineEdit_12.text())
        self.ui.listWidget.addItem(item)
    def addToList2(self):
        item = QListWidgetItem()
        item.setText(self.ui.lineEdit_13.text())
        self.ui.listWidget_2.addItem(item)
    def addToList3(self):
        item = QListWidgetItem()
        item.setText(self.ui.lineEdit_14.text())
        self.ui.listWidget_3.addItem(item)
        
        
    def removePkg(self):
        item = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(item)
    def addPkg(self):
        item = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(item)
    
    def setPkgName(self):
        self.ui.lineEdit.setText(self.ui.lineEdit.text().replace(" ","-").lower())    
    
    def loadUi(self):
        self.ui.lineEdit.setText(Settings.projectName.replace(" ", "-").lower())
        self.conf = configparser.ConfigParser()
        self.conf.read(Settings.projectConf)
        if self.conf.has_option("Info", "GitHubRepo"):
            self.ui.lineEdit_4.setText(self.conf['Info']['GitHubRepo'])
        self.ui.lineEdit_9.setText(Settings.projectName + ' project file')
        self.ui.label_8.setText('Will save in /usr/share/doc/'+Settings.projectPkg+'/copyright')
        self.setPixmap(QWizard.LogoPixmap, QPixmap("icons/x-rpm.png"))
          
          
class RpmBuildProgressDialog(QDialog):
    def __init__(self, parent2):
        super(RpmBuildProgressDialog, self).__init__()
        self.ui = rpmProgressDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        movie = QMovie("./gifs/gear.gif")
        self.ui.label.setMovie(movie)
        movie.start()
        
        buildRPM = BuildRpmThread(self, parent2)
        buildRPM.procDone.connect(self.doneFunction)
        buildRPM.start()
        
        self.timer = TimerThread(self, 0.5)
        self.timer.signal.connect(self.updateLog)
        self.timer.start()
    
    def doneFunction(self):
        self.timer.exit()
        self.ui.textBrowser.moveCursor(QTextCursor.End)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Package builded, please click OK to save it ...")
        msgBox.setWindowTitle("BlackDevelop - RPM builder")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.close()
        
    def updateLog(self):
        with open("/usr/tmp/BlackDevelop_buildRpm.log", 'r') as f:
            self.ui.textBrowser.setPlainText(f.read())
            self.ui.textBrowser.moveCursor(QTextCursor.End)
            

class BuildRpmThread(QThread):
    procDone = pyqtSignal(bool)
    procProgress = pyqtSignal(int)
    def __init__(self, parent, parent2):
        QThread.__init__(self, parent)
        self.ui = parent2
        
    def run(self):
        self.script()
        self.procDone.emit(True)

    def script(self):
        print("BlackDev: rpmbuilder: preparing project ...")
                            
        if not p.isdir(p.join(Settings.projectPath, 'usr/share/doc/'+Settings.projectPkg)):
            os.makedirs(p.join(Settings.projectPath, 'usr/share/doc/'+Settings.projectPkg))
        with open(p.join(Settings.projectPath, 'usr/share/doc/'+Settings.projectPkg+'/COPYRIGHT'), 'w') as f:
            f.write(self.ui.plainTextEdit_2.toPlainText())
            
        if self.ui.groupBox_6.isChecked():
            xml = '''<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
   <mime-type type="'''+self.ui.lineEdit_8.text()+'''">
     <comment>'''+self.ui.lineEdit_9.text()+'''</comment>
     <glob pattern="'''+self.ui.lineEdit_10.text()+'''"/>
   </mime-type>
</mime-info>'''
            if not p.isdir(p.join(Settings.projectPath, 'usr/share/mime/packages/')):
                os.makedirs(p.join(Settings.projectPath, 'usr/share/mime/packages/'))
                with open(p.join(Settings.projectPath, 'usr/share/mime/packages/', self.ui.lineEdit_8.text().replace("/", "-") + ".xml"), 'w') as f:
                    f.write(xml)
            mime = "<mimetype>"+self.ui.lineEdit_8.text()+"</mimetype>"
        else:
            mime = ''
        
        if self.ui.groupBox_5.isChecked():
            mimetypes = ''
            mime = ''
            for item in range(self.ui.listWidget_3.count()):
                item = self.ui.listWidget_3.item(item)
                if mime == '':
                    mime = item.text()
                elif mime[-2:] == ", ":
                    mime = mime + ", " + item.text()
                else:
                    mime = mime + ", " + item.text()
                if mimetypes == '':
                    mimetypes = "<mimetype>"+item.text()+"</mimetype>"
                else:
                    mimetypes = mimetypes + '\n<mimetype>'+item.text()+'</mimetype>'
                    
            mime = "MimeTypes=" + mime
            print(mime)
        if self.ui.groupBox_4.isChecked():
            screenshots = ''
            for item in range(self.ui.listWidget_2.count()):
                item = self.ui.listWidget_2.item(item)
                if screenshots == '':
                    screenshots = '<image type="source" width="800" height="600">'+item.text()+'</image>'
                else:
                    screenshots = screenshots + '\n<image type="source" width="800" height="600">'+item.text()+'</image>'
        else:
            screenshots = ''  
        if self.ui.groupBox_3.isChecked():
            keywords = ''
            for item in range(self.ui.listWidget.count()):
                item = self.ui.listWidget.item(item)
                if keywords == '':
                    keywords = '<keyword>'+item.text()+'</keyword>'
                else:
                    keywords = keywords + '\n<keyword>'+item.text()+'</keyword>'
        else:
            keywords = ''
        xml = '''​<?xml version="1.0"?>
​<components version="0.10">
​  <component type="desktop-application">
​    <id>'''+Settings.projectPkg+'''</id>
​    <pkgname>'''+self.ui.lineEdit.text()+'''</pkgname>
​    <name>'''+Settings.projectName+'''</name>
​    <summary>'''+self.ui.lineEdit_3.text()+'''</summary>
​    <keywords>
​      '''+keywords+'''
​    </keywords>
​    <icon type="cached">/'''+Settings.projectIcon+'''</icon>
​    <categories>
​      <category>'''+self.ui.comboBox_2.currentText()+'''</category>
​    </categories>
​    <mimetypes>
​      '''+mime+'''
​    </mimetypes>
​    <url type="homepage">'''+self.ui.lineEdit_4.text()+'''</url>
​    <screenshots>
​      <screenshot type="default">
​        '''+screenshots+'''
​      </screenshot>
​    </screenshots>
​  </component>
​</components>'''
        if not p.isdir(p.join(Settings.projectPath, 'usr/share/appdata/')):
            os.makedirs(p.join(Settings.projectPath, 'usr/share/appdata/'))
        file = p.join(Settings.projectPath, 'usr/share/appdata/', Settings.projectPkg + ".metainfo.xml")
        with open(file, 'w') as f:
            f.write(xml)
        if not p.isdir(p.join(Settings.projectPath, "usr/share/applications")):
            os.makedirs(p.join(Settings.projectPath, "usr/share/applications"))
        
        file = p.join(Settings.projectPath, "usr/share/applications", Settings.projectName.replace(" ","_") + ".desktop")
        desktop = '''[Desktop Entry]
Name='''+Settings.projectName+'''
Exec='''+p.join('/usr/bin', p.basename(Settings.projectExec).replace(".py","").lower().replace(" ",""))+'''
Icon=/'''+Settings.projectIcon+'''
Type=Application
Categories='''+self.ui.comboBox_2.currentText()+''';        
''' + mime
        with open(file, 'w') as f:
            f.write(desktop)
        self.procProgress.emit(10)
        print('BlackDev: rpmbuilder: Preparing project for PyInstaller ...')
        self.fixPath()
        self.procProgress.emit(15)                
        print("BlackDev: rpmbuilder: Compiling (PyInstaller) ...")
        os.chdir(Settings.projectSrc)
        os.system('pyinstaller --onefile --windowed "' +p.join(Settings.projectPath, Settings.projectExec)+ '" 2>> /usr/tmp/BlackDevelop_buildRpm.log')
        self.procProgress.emit(65)
        for exe in glob.glob(p.join(Settings.projectSrc, 'dist/*')):
            shutil.move(exe, p.join(p.dirname(exe), p.basename(exe.replace(" ", "").lower())))
            exe = p.join(p.dirname(exe), p.basename(exe.replace(" ", "").lower()))
        print('BlackDev: rpmbuilder: Preparing project to build RPM package...')
        if not p.isdir(p.join(Settings.projectPath, "usr/bin")):
            os.makedirs(p.join(Settings.projectPath, "usr/bin"))
        else:
            shutil.rmtree(p.join(Settings.projectPath, "usr/bin"))
            os.makedirs(p.join(Settings.projectPath, "usr/bin"))
        shutil.move(exe, p.join(Settings.projectPath, "usr/bin"))
        projectFiles = ''
        print('BlackDev: rpmbuilder: Clearing ...')
        if p.isdir(p.join(p.expanduser('~'), 'rpmbuild')):
            shutil.rmtree(p.join(p.expanduser('~'), 'rpmbuild'))
        shutil.rmtree(p.join(Settings.projectSrc, "build"))
        shutil.rmtree(p.join(Settings.projectSrc, "__pycache__"))
        os.remove(p.join(Settings.projectSrc, Settings.projectName+".spec"))
        shutil.rmtree(p.join(Settings.projectSrc, "dist"))
        projectFiles = ''
        for root, dirs, files in os.walk(Settings.projectPath):
            for file in files:
                file = p.join(root, file)
                file = file.replace(Settings.projectPath, "")
                if projectFiles == '' and not p.basename(file) == ".BlackDevelop.conf":
                    projectFiles = '\n"'+file + '"' 
                elif not p.basename(file) == ".BlackDevelop.conf":
                    projectFiles = projectFiles + '\n"'+file + '"'
        Requires='Requires:    '
        for item in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(item)
            if Requires == '':
                Requires = item.text()
            elif Requires[-2:] == ", ":
                Requires = Requires + ", " + item.text()
            else:
                Requires = Requires + ", " + item.text()
        if Requires == 'Requires:    ':
            Requires = ""
        os.chdir(p.expanduser('~'))
        spec = '''Name:    '''+self.ui.lineEdit.text()+'''
Version:    '''+Settings.projectVersion+'''
Release:    '''+self.ui.lineEdit_2.text()+'''
Summary:    '''+self.ui.lineEdit_3.text()+'''
License:    '''+self.ui.lineEdit_5.text()+'''
Url:    '''+self.ui.lineEdit_4.text()+'''
BuildArch:    '''+self.ui.comboBox.currentText()+'''

'''+Requires+'''

%description
'''+self.ui.plainTextEdit.toPlainText()+'''

%prep


%build


%install
mkdir -p %{buildroot}/
cp -r ./* %buildroot/

%files
'''+projectFiles+'''

%clean

%changelog

%check

%post
'''+self.ui.plainTextEdit_4.toPlainText()+'''
%pre
'''+self.ui.plainTextEdit_3.toPlainText()+'''
%preun
'''+self.ui.plainTextEdit_5.toPlainText()+'''
%postun
'''+self.ui.plainTextEdit_6.toPlainText()
        os.system("rpmdev-setuptree")
        open(p.join(p.expanduser('~'), 'rpmbuild/SPECS/'+Settings.projectPkg+'.spec'), 'a').close()
        with open(p.join(p.expanduser('~'), 'rpmbuild/SPECS/'+Settings.projectPkg+'.spec'), 'w') as f:
            f.write(spec)
        for dir in glob.glob(Settings.projectPath + "/*"):
            if not dir == ".BlackDevelop.conf":
                shutil.move(p.join(Settings.projectPath, dir), "rpmbuild/BUILD")
        print('BlackDev: rpmbuilder: Building RPM ...')
        os.system('rpmbuild -bb --define "%_build_id_links none" --define "debug_package %{nil}" "'+ p.join(p.expanduser('~'), 'rpmbuild/SPECS/'+Settings.projectPkg+'.spec" 2>> /usr/tmp/BlackDevelop_buildRpm.log'))
        self.procProgress.emit(95)
        print('BlackDev: rpmbuilder: Clearing ...')
        for dir in glob.glob("rpmbuild/BUILD/*"):
            shutil.move(dir, Settings.projectPath)                  
        self.procProgress.emit(100)
        
    def fixPath(self):
        os.chdir(Settings.projectPath)
        for root, dirs, files in os.walk(Settings.projectPath):
            for file in files:
                file = p.join(root, file)
                filedata = ''
                if p.isdir(file):
                    continue
                try:
                    with open(p.join(root, file), 'r') as f :
                        filedata = f.read()
                except:
                    continue
                paths = filedata.split('"')
                if not len(paths) == 1:
                    newfile = ""
                    
                    for data in paths:
                        
                        if p.exists(data) and data[-4:] == '.png' and not Settings.projectPath in p.normpath(data):
                            pixmaps = p.join(Settings.projectSrc, 'pixmaps')
                            if not p.isdir(pixmaps):
                                os.makedirs(pixmaps)
                                
                            pixmap = p.join(pixmaps, p.basename(p.normpath(data)))
                            if not p.isfile(pixmap):
                                shutil.copy2(p.normpath(data), pixmaps)
                            pixmap = pixmap.replace(Settings.projectPath, "")
                            filedata = filedata.replace(data, pixmap)
                        elif p.exists(p.join(Settings.projectSrc, data[2:])) and data[:2] == "./":
                            oldpath = p.join(Settings.projectSrc, data[2:])
                            newpath = p.join(oldpath.replace(Settings.projectPath, ""))
                            filedata = filedata.replace(data, newpath)
                        elif p.exists(data) and file[-3:] == '.py' and Settings.projectPath in p.normpath(data):
                            newfile = p.abspath(data)
                            newfile = newfile.replace(Settings.projectPath, "")
                            filedata = filedata.replace(data, newfile)
                        elif p.exists(p.join(Settings.projectPath, data)) and not data == "":
                            newfile = '/' + data
                            filedata = filedata.replace(data, newfile)
                                
                    if file[-3:] == '.py' and not filedata == '':
                        with open(p.join(root, file), 'w') as f:
                            f.write(filedata)
    

class importedFromGit(object):
    def __init__(self):
        super(importedFromGit, self).__init__()    

def removeOldProject():
    shutil.rmtree(Settings.projectPath)
    shutil.move(Settings.projectPath + ".old", Settings.projectPath)    

def createOldProject():
    shutil.copytree(Settings.projectPath, Settings.projectPath + ".old")    

def tardir(path, tar_name):
    os.chdir(p.join(Settings.projectPath, "usr/src", Settings.projectPkg))
    with tarfile.open(p.basename(tar_name), "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                arcname = p.join(root, file)
                arcname = arcname.replace(p.join(Settings.projectPath, "usr/src"), "")
                tar_handle.add(p.join(root, file), arcname)

    shutil.move(p.basename(tar_name), tar_name)
    
    
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def extract(tar_url, extract_path='.'):
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract(item.name, "./" + item.name[:item.name.rfind('/')])
app = QApplication(sys.argv)
ui = selectProjectDialog()
ui.show()
sys.exit(app.exec_())
