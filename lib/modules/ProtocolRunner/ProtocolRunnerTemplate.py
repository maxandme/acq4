# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProtocolRunnerTemplate.ui'
#
# Created: Tue Apr 21 16:19:39 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1118, 593)
        MainWindow.setStyleSheet("""QDockWidget::title { background-color: #446; color: #DDD }
QDockWidget > QWidget { background-color: #BBB }
QMainWindow { background-color: #000 }
QSplitter::handle {background-color: #666}
QMainWindow::separator {background-color: #666}""")
        MainWindow.setDockNestingEnabled(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.LoaderDock = QtGui.QDockWidget(MainWindow)
        self.LoaderDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.LoaderDock.setObjectName("LoaderDock")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_5 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.newProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.newProtocolBtn.setObjectName("newProtocolBtn")
        self.gridLayout_5.addWidget(self.newProtocolBtn, 1, 1, 1, 1)
        self.loadProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.loadProtocolBtn.setObjectName("loadProtocolBtn")
        self.gridLayout_5.addWidget(self.loadProtocolBtn, 2, 1, 1, 1)
        self.saveProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.saveProtocolBtn.setEnabled(False)
        self.saveProtocolBtn.setObjectName("saveProtocolBtn")
        self.gridLayout_5.addWidget(self.saveProtocolBtn, 3, 1, 1, 1)
        self.saveAsProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.saveAsProtocolBtn.setEnabled(True)
        self.saveAsProtocolBtn.setObjectName("saveAsProtocolBtn")
        self.gridLayout_5.addWidget(self.saveAsProtocolBtn, 4, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 77, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 6, 1, 1, 1)
        self.deleteProtocolBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.deleteProtocolBtn.setEnabled(False)
        self.deleteProtocolBtn.setObjectName("deleteProtocolBtn")
        self.gridLayout_5.addWidget(self.deleteProtocolBtn, 5, 1, 1, 1)
        self.protocolList = QtGui.QTreeView(self.dockWidgetContents)
        self.protocolList.setObjectName("protocolList")
        self.gridLayout_5.addWidget(self.protocolList, 2, 0, 5, 1)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 1, 0, 1, 1)
        self.LoaderDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.LoaderDock)
        self.ProtocolDock = QtGui.QDockWidget(MainWindow)
        self.ProtocolDock.setEnabled(True)
        self.ProtocolDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.ProtocolDock.setObjectName("ProtocolDock")
        self.dockWidgetContents_5 = QtGui.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents_5)
        self.gridLayout.setObjectName("gridLayout")
        self.deviceList = QtGui.QListWidget(self.dockWidgetContents_5)
        self.deviceList.setObjectName("deviceList")
        self.gridLayout.addWidget(self.deviceList, 3, 0, 3, 2)
        self.label_8 = QtGui.QLabel(self.dockWidgetContents_5)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.protoDurationSpin = QtGui.QDoubleSpinBox(self.dockWidgetContents_5)
        self.protoDurationSpin.setObjectName("protoDurationSpin")
        self.gridLayout.addWidget(self.protoDurationSpin, 3, 2, 1, 1)
        self.protoContinuousCheck = QtGui.QCheckBox(self.dockWidgetContents_5)
        self.protoContinuousCheck.setObjectName("protoContinuousCheck")
        self.gridLayout.addWidget(self.protoContinuousCheck, 4, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 91, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 2, 1, 1)
        self.testSingleBtn = QtGui.QPushButton(self.dockWidgetContents_5)
        self.testSingleBtn.setEnabled(False)
        self.testSingleBtn.setObjectName("testSingleBtn")
        self.gridLayout.addWidget(self.testSingleBtn, 6, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        self.runProtocolBtn = QtGui.QPushButton(self.dockWidgetContents_5)
        self.runProtocolBtn.setEnabled(False)
        self.runProtocolBtn.setObjectName("runProtocolBtn")
        self.gridLayout.addWidget(self.runProtocolBtn, 6, 2, 1, 1)
        self.label = QtGui.QLabel(self.dockWidgetContents_5)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.ProtocolDock.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.ProtocolDock)
        self.SequenceDock = QtGui.QDockWidget(MainWindow)
        self.SequenceDock.setEnabled(False)
        self.SequenceDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.SequenceDock.setObjectName("SequenceDock")
        self.dockWidgetContents_7 = QtGui.QWidget()
        self.dockWidgetContents_7.setObjectName("dockWidgetContents_7")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents_7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sequenceParamList = QtGui.QListWidget(self.dockWidgetContents_7)
        self.sequenceParamList.setObjectName("sequenceParamList")
        self.gridLayout_2.addWidget(self.sequenceParamList, 0, 0, 6, 2)
        self.seqParamUpBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.seqParamUpBtn.setObjectName("seqParamUpBtn")
        self.gridLayout_2.addWidget(self.seqParamUpBtn, 0, 2, 1, 1)
        self.seqParamDnBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.seqParamDnBtn.setObjectName("seqParamDnBtn")
        self.gridLayout_2.addWidget(self.seqParamDnBtn, 1, 2, 1, 1)
        self.seqParamGroupBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.seqParamGroupBtn.setObjectName("seqParamGroupBtn")
        self.gridLayout_2.addWidget(self.seqParamGroupBtn, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents_7)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 2, 1, 1)
        self.paramSpaceLabel = QtGui.QLabel(self.dockWidgetContents_7)
        self.paramSpaceLabel.setObjectName("paramSpaceLabel")
        self.gridLayout_2.addWidget(self.paramSpaceLabel, 4, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 77, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 5, 2, 1, 1)
        self.testSequenceBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.testSequenceBtn.setObjectName("testSequenceBtn")
        self.gridLayout_2.addWidget(self.testSequenceBtn, 6, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(146, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 6, 1, 1, 1)
        self.runSequenceBtn = QtGui.QPushButton(self.dockWidgetContents_7)
        self.runSequenceBtn.setObjectName("runSequenceBtn")
        self.gridLayout_2.addWidget(self.runSequenceBtn, 6, 2, 1, 1)
        self.SequenceDock.setWidget(self.dockWidgetContents_7)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.SequenceDock)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.LoaderDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Loader", None, QtGui.QApplication.UnicodeUTF8))
        self.newProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.loadProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.saveProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Save As..", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Protocols", None, QtGui.QApplication.UnicodeUTF8))
        self.ProtocolDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Protocol", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Duration", None, QtGui.QApplication.UnicodeUTF8))
        self.protoContinuousCheck.setText(QtGui.QApplication.translate("MainWindow", "Continuous", None, QtGui.QApplication.UnicodeUTF8))
        self.testSingleBtn.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.runProtocolBtn.setText(QtGui.QApplication.translate("MainWindow", "Run Protocol", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.SequenceDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.seqParamUpBtn.setText(QtGui.QApplication.translate("MainWindow", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.seqParamDnBtn.setText(QtGui.QApplication.translate("MainWindow", "Dn", None, QtGui.QApplication.UnicodeUTF8))
        self.seqParamGroupBtn.setText(QtGui.QApplication.translate("MainWindow", "Group", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Parameter Space: ", None, QtGui.QApplication.UnicodeUTF8))
        self.testSequenceBtn.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.runSequenceBtn.setText(QtGui.QApplication.translate("MainWindow", "Run Sequence", None, QtGui.QApplication.UnicodeUTF8))

