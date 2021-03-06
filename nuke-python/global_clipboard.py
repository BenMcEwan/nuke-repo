import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from PySide.QtGui import QApplication, QCompleter, QLineEdit, QStringListModel
import os
import glob

import nuke


class global_clipboard():

    def __init__(self):
        self.repo = "T://_Nuke_tools//global_clipboard//"
        self.saveName = "tempClipBoard"
        self.user = os.environ.get("USERNAME")
        self.savePath = self.repo + self.saveName+"_"+self.user+".nk"
        
    def paste(self, getUser):
        self.loadPath = self.repo + self.saveName+"_"+getUser+".nk"
        nuke.nodePaste(self.loadPath)
    
    def copy(self):
        nuke.nodeCopy(self.savePath)
        print "Selected nodes saved to "+ self.savePath


class GlobalClipboard(QtGui.QDialog):
    def __init__(self):
        def paste():
            loadPath = (self.repository+self.filename_base+"%s.nk")%(self.cb_list.currentText())
            print loadPath
            nuke.nodePaste(loadPath)
            self.close()
        self.user = os.environ.get("USERNAME")
        self.repository = "T://_Nuke_tools//global_clipboard//"
        self.filename_base = "tempClipBoard_"

        os.chdir(self.repository)
        self.items = []
        for file in glob.glob("*.nk"):
            self.items.append(file.split(self.filename_base)[-1].split('.')[0])
        super(GlobalClipboard, self).__init__(QtGui.QApplication.activeWindow())
        self.setWindowTitle('Global Clipboard')
        self.hbox=QtGui.QHBoxLayout()

        self.cb_list=QtGui.QComboBox()
        self.cb_list.setEditable(True)
        for item in self.items:
            self.cb_list.addItem(item)

        self.completer = QCompleter()
        self.cb_list.setCompleter(self.completer)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        model_autocomplete = QStringListModel()
        self.completer.setModel(model_autocomplete)
        model_autocomplete.setStringList(self.items)

        self.description=QtGui.QLabel(self)
        self.description.setText("Paste from")
        self.hbox.addWidget(self.description)#desc

        self.hbox.addWidget(self.cb_list)#menu

        self.button=QtGui.QPushButton("Paste")
        self.hbox.addWidget(self.button)#button
        self.button.clicked.connect(paste)

        self.setLayout(self.hbox)

    def copy(self):
        savePath = (self.repository+self.filename_base+"%s.nk")%(self.user)
        nuke.nodeCopy(savePath)
        print "Selected nodes saved to "+ savePath

    def showDialog(self):
        wnd = GlobalClipboard()
        wnd.show()