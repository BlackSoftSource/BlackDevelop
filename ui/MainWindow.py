# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 728)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 970, 29))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuImport = QtWidgets.QMenu(self.menuProject)
        icon = QtGui.QIcon.fromTheme("albumfolder-importdir")
        self.menuImport.setIcon(icon)
        self.menuImport.setObjectName("menuImport")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuLaunch = QtWidgets.QMenu(self.menubar)
        self.menuLaunch.setObjectName("menuLaunch")
        self.menuDistribution = QtWidgets.QMenu(self.menubar)
        self.menuDistribution.setObjectName("menuDistribution")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuNew = QtWidgets.QMenu(self.menuFile)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.menuNew.setIcon(icon)
        self.menuNew.setObjectName("menuNew")
        self.menuGraphical_interface = QtWidgets.QMenu(self.menuNew)
        icon = QtGui.QIcon.fromTheme("window")
        self.menuGraphical_interface.setIcon(icon)
        self.menuGraphical_interface.setObjectName("menuGraphical_interface")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeView.setDragEnabled(True)
        self.treeView.setDragDropOverwriteMode(True)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.treeView.setDefaultDropAction(QtCore.Qt.TargetMoveAction)
        self.treeView.setAlternatingRowColors(False)
        self.treeView.setSortingEnabled(True)
        self.treeView.setExpandsOnDoubleClick(True)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.dockWidget_3 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_3)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setFloating(False)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_2)
        self.actionPython3 = QtWidgets.QAction(MainWindow)
        self.actionPython3.setObjectName("actionPython3")
        self.actionNew_2 = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNew_2.setIcon(icon)
        self.actionNew_2.setObjectName("actionNew_2")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.actionExit.setIcon(icon)
        self.actionExit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionExit.setObjectName("actionExit")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-save")
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-save-as")
        self.actionSave_as.setIcon(icon)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionBlackDevelop_settings = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("preferences-desktop")
        self.actionBlackDevelop_settings.setIcon(icon)
        self.actionBlackDevelop_settings.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.actionBlackDevelop_settings.setObjectName("actionBlackDevelop_settings")
        self.actionProject_settings = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-properties")
        self.actionProject_settings.setIcon(icon)
        self.actionProject_settings.setObjectName("actionProject_settings")
        self.actionRun_program = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.actionRun_program.setIcon(icon)
        self.actionRun_program.setObjectName("actionRun_program")
        self.actionBuild_and_run = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("debug-run")
        self.actionBuild_and_run.setIcon(icon)
        self.actionBuild_and_run.setObjectName("actionBuild_and_run")
        self.actionBuild_RPM_package = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("application-x-rpm")
        self.actionBuild_RPM_package.setIcon(icon)
        self.actionBuild_RPM_package.setObjectName("actionBuild_RPM_package")
        self.actionBuild_tar_gz_source = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("package-x-generic")
        self.actionBuild_tar_gz_source.setIcon(icon)
        self.actionBuild_tar_gz_source.setObjectName("actionBuild_tar_gz_source")
        self.actionUpload_to_packagecloud_io_and_build_RPM = QtWidgets.QAction(MainWindow)
        self.actionUpload_to_packagecloud_io_and_build_RPM.setObjectName("actionUpload_to_packagecloud_io_and_build_RPM")
        self.actionFrom_tgz = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("package-x-generic")
        self.actionFrom_tgz.setIcon(icon)
        self.actionFrom_tgz.setObjectName("actionFrom_tgz")
        self.actionFrom_GitHub = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/icons/x-github.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFrom_GitHub.setIcon(icon)
        self.actionFrom_GitHub.setObjectName("actionFrom_GitHub")
        self.actionFrom_SourceForge_com = QtWidgets.QAction(MainWindow)
        self.actionFrom_SourceForge_com.setObjectName("actionFrom_SourceForge_com")
        self.actionAbout_BlackDevelop = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("help-about")
        self.actionAbout_BlackDevelop.setIcon(icon)
        self.actionAbout_BlackDevelop.setMenuRole(QtWidgets.QAction.AboutRole)
        self.actionAbout_BlackDevelop.setObjectName("actionAbout_BlackDevelop")
        self.actionQbout_Qt5 = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("qtlogo")
        self.actionQbout_Qt5.setIcon(icon)
        self.actionQbout_Qt5.setMenuRole(QtWidgets.QAction.AboutQtRole)
        self.actionQbout_Qt5.setObjectName("actionQbout_Qt5")
        self.actionDirectories = QtWidgets.QAction(MainWindow)
        self.actionDirectories.setCheckable(True)
        self.actionDirectories.setChecked(True)
        self.actionDirectories.setObjectName("actionDirectories")
        self.actionGitHub = QtWidgets.QAction(MainWindow)
        self.actionGitHub.setIcon(icon)
        self.actionGitHub.setIconVisibleInMenu(True)
        self.actionGitHub.setObjectName("actionGitHub")
        self.actionSourceforge = QtWidgets.QAction(MainWindow)
        self.actionSourceforge.setObjectName("actionSourceforge")
        self.actionLog = QtWidgets.QAction(MainWindow)
        self.actionLog.setCheckable(True)
        self.actionLog.setChecked(True)
        self.actionLog.setObjectName("actionLog")
        self.actionImport = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.actionImport.setIcon(icon)
        self.actionImport.setObjectName("actionImport")
        self.actionBash_script = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("utilities-terminal")
        self.actionBash_script.setIcon(icon)
        self.actionBash_script.setObjectName("actionBash_script")
        self.actionText_document = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("text-x-generic")
        self.actionText_document.setIcon(icon)
        self.actionText_document.setObjectName("actionText_document")
        self.actionPackage = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("package-x-generic")
        self.actionPackage.setIcon(icon)
        self.actionPackage.setObjectName("actionPackage")
        self.actionModule = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("text-x-generic")
        self.actionModule.setIcon(icon)
        self.actionModule.setObjectName("actionModule")
        self.actionAll_files = QtWidgets.QAction(MainWindow)
        self.actionAll_files.setCheckable(True)
        self.actionAll_files.setChecked(False)
        self.actionAll_files.setObjectName("actionAll_files")
        self.actionModules = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("x-package-repository")
        self.actionModules.setIcon(icon)
        self.actionModules.setObjectName("actionModules")
        self.actionMainWindow = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("window")
        self.actionMainWindow.setIcon(icon)
        self.actionMainWindow.setObjectName("actionMainWindow")
        self.actionDialog = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("window")
        self.actionDialog.setIcon(icon)
        self.actionDialog.setObjectName("actionDialog")
        self.actionWizard = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("window")
        self.actionWizard.setIcon(icon)
        self.actionWizard.setObjectName("actionWizard")
        self.actionBuild = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("run-build")
        self.actionBuild.setIcon(icon)
        self.actionBuild.setObjectName("actionBuild")
        self.actionSource_directory = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("inode-directory")
        self.actionSource_directory.setIcon(icon)
        self.actionSource_directory.setObjectName("actionSource_directory")
        self.actionRename = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edit-rename")
        self.actionRename.setIcon(icon)
        self.actionRename.setObjectName("actionRename")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionErrors = QtWidgets.QAction(MainWindow)
        self.actionErrors.setCheckable(True)
        self.actionErrors.setObjectName("actionErrors")
        self.actionClose = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("project-development-close")
        self.actionClose.setIcon(icon)
        self.actionClose.setObjectName("actionClose")
        self.menuImport.addAction(self.actionFrom_tgz)
        self.menuImport.addAction(self.actionFrom_GitHub)
        self.menuProject.addAction(self.actionNew_2)
        self.menuProject.addAction(self.actionOpen)
        self.menuProject.addAction(self.actionSave)
        self.menuProject.addAction(self.actionSave_as)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.menuImport.menuAction())
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionClose)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionBlackDevelop_settings)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionProject_settings)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionModules)
        self.menuLaunch.addAction(self.actionRun_program)
        self.menuLaunch.addSeparator()
        self.menuLaunch.addAction(self.actionBuild_and_run)
        self.menuLaunch.addSeparator()
        self.menuLaunch.addAction(self.actionBuild)
        self.menuDistribution.addAction(self.actionBuild_RPM_package)
        self.menuDistribution.addSeparator()
        self.menuDistribution.addAction(self.actionBuild_tar_gz_source)
        self.menuDistribution.addAction(self.actionGitHub)
        self.menuHelp.addAction(self.actionAbout_BlackDevelop)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionQbout_Qt5)
        self.menuView.addAction(self.actionDirectories)
        self.menuView.addAction(self.actionLog)
        self.menuView.addAction(self.actionErrors)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionAll_files)
        self.menuGraphical_interface.addAction(self.actionMainWindow)
        self.menuGraphical_interface.addAction(self.actionDialog)
        self.menuGraphical_interface.addAction(self.actionWizard)
        self.menuNew.addAction(self.actionSource_directory)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionText_document)
        self.menuNew.addAction(self.actionBash_script)
        self.menuNew.addSeparator()
        self.menuNew.addAction(self.actionPackage)
        self.menuNew.addAction(self.actionModule)
        self.menuNew.addAction(self.menuGraphical_interface.menuAction())
        self.menuFile.addAction(self.menuNew.menuAction())
        self.menuFile.addAction(self.actionRename)
        self.menuFile.addAction(self.actionDelete)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuLaunch.menuAction())
        self.menubar.addAction(self.menuDistribution.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        self.actionLog.triggered['bool'].connect(self.dockWidget_3.setVisible)
        self.actionDirectories.triggered['bool'].connect(self.dockWidget.setVisible)
        self.actionErrors.triggered['bool'].connect(self.dockWidget_2.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BlackDevelop"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuImport.setTitle(_translate("MainWindow", "Import from"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuLaunch.setTitle(_translate("MainWindow", "Launch"))
        self.menuDistribution.setTitle(_translate("MainWindow", "Distribution"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuFile.setTitle(_translate("MainWindow", "Files"))
        self.menuNew.setTitle(_translate("MainWindow", "New"))
        self.menuGraphical_interface.setTitle(_translate("MainWindow", "Graphical window"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Files"))
        self.dockWidget_3.setWindowTitle(_translate("MainWindow", "Log"))
        self.dockWidget_2.setWindowTitle(_translate("MainWindow", "BlackDevelop errors"))
        self.actionPython3.setText(_translate("MainWindow", "Python3"))
        self.actionNew_2.setText(_translate("MainWindow", "New"))
        self.actionNew_2.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as ..."))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionBlackDevelop_settings.setText(_translate("MainWindow", "BlackDevelop settings ..."))
        self.actionProject_settings.setText(_translate("MainWindow", "Project settings ..."))
        self.actionRun_program.setText(_translate("MainWindow", "Run"))
        self.actionRun_program.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionBuild_and_run.setText(_translate("MainWindow", "Build and run"))
        self.actionBuild_and_run.setShortcut(_translate("MainWindow", "Ctrl+Shift+R"))
        self.actionBuild_RPM_package.setText(_translate("MainWindow", "Build RPM package ..."))
        self.actionBuild_tar_gz_source.setText(_translate("MainWindow", "Export .tar.gz source ..."))
        self.actionUpload_to_packagecloud_io_and_build_RPM.setText(_translate("MainWindow", "Upload to packagecloud.io and build RPM (auto-updating) ..."))
        self.actionFrom_tgz.setText(_translate("MainWindow", ".tgz ..."))
        self.actionFrom_GitHub.setText(_translate("MainWindow", "GitHub ..."))
        self.actionFrom_SourceForge_com.setText(_translate("MainWindow", "From sourceforge.net"))
        self.actionAbout_BlackDevelop.setText(_translate("MainWindow", "About BlackDevelop"))
        self.actionQbout_Qt5.setText(_translate("MainWindow", "Qbout Qt5"))
        self.actionDirectories.setText(_translate("MainWindow", "Files"))
        self.actionGitHub.setText(_translate("MainWindow", "Push to GitHub"))
        self.actionGitHub.setIconText(_translate("MainWindow", "Upload to GitHub"))
        self.actionGitHub.setStatusTip(_translate("MainWindow", "Upload to GitHub"))
        self.actionSourceforge.setText(_translate("MainWindow", "Sourceforge"))
        self.actionLog.setText(_translate("MainWindow", "Log"))
        self.actionImport.setText(_translate("MainWindow", "Import ..."))
        self.actionImport.setIconText(_translate("MainWindow", "Import file"))
        self.actionImport.setStatusTip(_translate("MainWindow", "Import file"))
        self.actionImport.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionBash_script.setText(_translate("MainWindow", "Bash script"))
        self.actionText_document.setText(_translate("MainWindow", "Text document"))
        self.actionPackage.setText(_translate("MainWindow", "Package"))
        self.actionPackage.setStatusTip(_translate("MainWindow", "New package"))
        self.actionModule.setText(_translate("MainWindow", "Module"))
        self.actionModule.setStatusTip(_translate("MainWindow", "New module"))
        self.actionAll_files.setText(_translate("MainWindow", "All files"))
        self.actionAll_files.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionModules.setText(_translate("MainWindow", "Modules ..."))
        self.actionMainWindow.setText(_translate("MainWindow", "MainWindow"))
        self.actionDialog.setText(_translate("MainWindow", "Dialog"))
        self.actionDialog.setStatusTip(_translate("MainWindow", "Add dialog window"))
        self.actionWizard.setText(_translate("MainWindow", "Wizard"))
        self.actionBuild.setText(_translate("MainWindow", "Build"))
        self.actionBuild.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actionSource_directory.setText(_translate("MainWindow", "Source directory"))
        self.actionRename.setText(_translate("MainWindow", "Rename"))
        self.actionDelete.setText(_translate("MainWindow", "Move to trash"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del"))
        self.actionErrors.setText(_translate("MainWindow", "Errors"))
        self.actionClose.setText(_translate("MainWindow", "Close project"))
