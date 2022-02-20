#pyuic5 -x gui.ui -o guitest2.py

from distutils.log import error
from tracemalloc import start
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import  QApplication,QTableView,QMainWindow, QTableWidgetItem,QFileDialog,QWidget,QMenu
import  pandas as pd
from io import StringIO
import altair as alt
from PyQt5.QtCore import QDataStream, Qt ,QEvent
import json
import os.path

import sys

class headTopic:  
    def __init__(self): 
        self.data_head = {} 
               
    def get_backup(self):
        if os.path.exists('data_head.json') == False:
            self.backup_head()        
        with open('data_head.json','r') as head_file:
            self.data_head = json.load(head_file)
        return self.data_head
    
    def backup_head(self):
        with open('data_head.json', 'w') as head_file:
            json.dump(self.data_head, head_file)
            

            
class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().profile().downloadRequested.connect(self.onDownloadRequested)
        self.windows = []

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def onDownloadRequested(self, download):
        if (
            download.state()
            == QtWebEngineWidgets.QWebEngineDownloadItem.DownloadRequested
        ):
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, self.tr("Save as"), download.path()
            )
            if path:
                download.setPath(path)
                download.accept()

    def createWindow(self, type_):
        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            window = QtWidgets.QMainWindow(self)
            view = QtWebEngineWidgets.QWebEngineView(window)            
            window.resize(641, 471)
            window.setCentralWidget(view)
            window.show()
            return view

    def updateChart(self, chart, **kwargs):
        output = StringIO()
        chart.save(output, "html", **kwargs)
        self.setHtml(output.getvalue())

class HeadList(QtWidgets.QListWidget):
    def __init__(self, main, parent):
        super().__init__(parent)
        self.main = main
        
    def readData(self, mime: QtCore.QMimeData) -> list:
        self.stream = QDataStream(mime.data('application/x-qabstractitemmodeldatalist'))
        textList = []
        while not self.stream.atEnd():
            # we're not using row and columns, but we *must* read them
            row = self.stream.readInt()
            col = self.stream.readInt()
            for dataSize in range(self.stream.readInt()):
                role, value = self.stream.readInt(), self.stream.readQVariant()
                if role == Qt.DisplayRole:
                    textList.append(value)
        return textList[0]

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        super().dropEvent(event)
        self.main.update_head()
        
class Ui_Filter_Window(object):
    def __init__(self):
        
        self.getdatafilter = Ui_MainWindow()
        
        
        
    def setupUi(self,item_head, Filter_Window,listWidget,all_data):
        Filter_Window.setObjectName("Filter_Window")
        Filter_Window.resize(412, 575)
        self.centralwidget = QtWidgets.QWidget(Filter_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 391, 481))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 41))
        self.label.setObjectName("label")
        self.Apply = QtWidgets.QPushButton(self.centralwidget)
        self.Apply.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.Apply.setObjectName("Apply")

        self.Remove_all = QtWidgets.QPushButton(self.centralwidget)
        self.Remove_all.setGeometry(QtCore.QRect(200, 20, 75, 23))
        self.Remove_all.setObjectName("Remove_all")

        self.Select_all = QtWidgets.QPushButton(self.centralwidget)
        self.Select_all.setGeometry(QtCore.QRect(100, 20, 75, 23))
        self.Select_all.setObjectName("Select_all")

        Filter_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Filter_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 21))
        self.menubar.setObjectName("menubar")
        Filter_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Filter_Window)
        self.statusbar.setObjectName("statusbar")
        Filter_Window.setStatusBar(self.statusbar)

        self.filterdata(listWidget,all_data)
        
        

        
        self.Apply.clicked.connect(lambda :self.filterComplete(item_head))
        self.Remove_all.clicked.connect(self.clear_all)
        self.Select_all.clicked.connect(self.select_all)
        self.retranslateUi(Filter_Window)
        QtCore.QMetaObject.connectSlotsByName(Filter_Window)

    def retranslateUi(self, Filter_Window):
        _translate = QtCore.QCoreApplication.translate
        Filter_Window.setWindowTitle(_translate("Filter_Window", "MainWindow"))
        self.label.setText(_translate("Filter_Window", "LIST HEADER"))
        self.Apply.setText(_translate("Filter_Window", "Apply"))
        self.Remove_all.setText(_translate("Filter_Window", "Remove All"))
        self.Select_all.setText(_translate("Filter_Window", "Select All"))

    def filterdata(self,listWidget,all_data):
        all_data = all_data
        
        item2 = listWidget.currentItem().text()
        for i in all_data[item2].unique():
            self.item = QtWidgets.QListWidgetItem(i)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.item.setCheckState(QtCore.Qt.Checked)
            self.listWidget.addItem(self.item)       



    def filterComplete(self,item_head):
        self.getCheckItem = []
        self.getCheckItem.clear()
        self.item = item_head
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).checkState() != QtCore.Qt.Checked : #send Signal not check 
                self.getCheckItem.append(self.listWidget.item(i).text())
        Ui_MainWindow.getDataFilter(self,self.getCheckItem,self.item)
        
        
    def clear_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setCheckState(~(QtCore.Qt.Checked))      

    def select_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setCheckState(QtCore.Qt.Checked)         
######################
        
                

## y/m/d       
class Ui_Filter_date_Window(object):
    def setupUi(self,item_head,Filter_Window,listWidget,all_data):
        Filter_Window.setObjectName("Filter_Window")
        Filter_Window.resize(589, 575)
        self.centralwidget = QtWidgets.QWidget(Filter_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 391, 481))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 41))
        self.label.setObjectName("label")
        self.Apply = QtWidgets.QPushButton(self.centralwidget)
        self.Apply.setGeometry(QtCore.QRect(460, 360, 75, 23))
        self.Apply.setObjectName("Apply")
        self.Add_ALL_2 = QtWidgets.QPushButton(self.centralwidget)
        self.Add_ALL_2.setGeometry(QtCore.QRect(430, 80, 75, 23))
        self.Add_ALL_2.setObjectName("Add_ALL_2")
        self.Remove_ALL_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Remove_ALL_3.setGeometry(QtCore.QRect(430, 120, 75, 23))
        self.Remove_ALL_3.setObjectName("Remove_ALL_3")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(450, 220, 51, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(510, 220, 61, 31))
        self.textEdit.setObjectName("textEdit")
        self.Add_ALL_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Add_ALL_3.setGeometry(QtCore.QRect(460, 290, 75, 23))
        self.Add_ALL_3.setObjectName("Add_ALL_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 230, 41, 21))
        self.label_4.setObjectName("label_4")
        Filter_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Filter_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 21))
        self.menubar.setObjectName("menubar")
        Filter_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Filter_Window)
        self.statusbar.setObjectName("statusbar")
        Filter_Window.setStatusBar(self.statusbar)

        self.filterdata(listWidget,all_data)
        
        

        self.Add_ALL_3.clicked.connect(self.filter_date)
        self.Apply.clicked.connect(lambda :self.filterComplete(item_head))
        self.Add_ALL_2.clicked.connect(self.select_all)
        self.Remove_ALL_3.clicked.connect(self.clear_all)
        

        self.retranslateUi(Filter_Window)
        QtCore.QMetaObject.connectSlotsByName(Filter_Window)

    def retranslateUi(self, Filter_Window):
        _translate = QtCore.QCoreApplication.translate
        Filter_Window.setWindowTitle(_translate("Filter_Window", "Date Filter"))
        self.label.setText(_translate("Filter_Window", "LIST HEADER"))
        self.Apply.setText(_translate("Filter_Window", "Apply"))
        self.Add_ALL_2.setText(_translate("Filter_Window", "Add ALL"))
        self.Remove_ALL_3.setText(_translate("Filter_Window", "Remove ALL"))
        self.comboBox.setItemText(1, _translate("Filter_Window", ">"))
        self.comboBox.setItemText(2, _translate("Filter_Window", "<"))
        self.comboBox.setItemText(3, _translate("Filter_Window", "="))
        self.Add_ALL_3.setText(_translate("Filter_Window", "OK"))
        self.label_4.setText(_translate("Filter_Window", "Range"))       
        
    def filterdata(self,listWidget,all_data):
        all_data = all_data
        
        item2 = listWidget.currentItem().text()
        for i in all_data[item2].unique():
            self.item = QtWidgets.QListWidgetItem(i)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.item.setCheckState(QtCore.Qt.Checked)
            self.listWidget.addItem(self.item)       

    def filter_date(self):
        op = {">":(lambda x,y:x>y),"<":(lambda x,y:x<y),"=":(lambda x,y:x==y)}        
        if self.textEdit.toPlainText() == "" or  self.comboBox.currentText() == "":
            return
        for i in range(self.listWidget.count()):
            x = self.listWidget.item(i).text()
            y = self.textEdit.toPlainText()
            if  op[self.comboBox.currentText()](x,y):
                self.listWidget.item(i).setCheckState(QtCore.Qt.Checked)
            else:
                self.listWidget.item(i).setCheckState(~(QtCore.Qt.Checked))
                
    
    def clear_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setCheckState(~(QtCore.Qt.Checked))

    def select_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setCheckState(QtCore.Qt.Checked)                         

    def filterComplete(self,item_head):
        self.getCheckItem = []
        self.getCheckItem.clear()
        self.item = item_head
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).checkState() != QtCore.Qt.Checked : #send Signal not check 
                self.getCheckItem.append(self.listWidget.item(i).text())

        Ui_MainWindow.getDataFilter(self,self.getCheckItem,self.item)   

#all date
class Ui_Filter_Date_Window(object):
    def setupUi(self,item_head,Filter_Window,listWidget,all_data):
        Filter_Window.setObjectName("Filter_Window")
        Filter_Window.resize(589, 575)
        self.centralwidget = QtWidgets.QWidget(Filter_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 391, 481))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 41))
        self.label.setObjectName("label")
        self.Apply = QtWidgets.QPushButton(self.centralwidget)
        self.Apply.setGeometry(QtCore.QRect(460, 360, 75, 23))
        self.Apply.setObjectName("Apply")
        self.Add_ALL_2 = QtWidgets.QPushButton(self.centralwidget)
        self.Add_ALL_2.setGeometry(QtCore.QRect(430, 80, 75, 23))
        self.Add_ALL_2.setObjectName("Add_ALL_2")
        self.Remove_ALL_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Remove_ALL_3.setGeometry(QtCore.QRect(430, 120, 75, 23))
        self.Remove_ALL_3.setObjectName("Remove_ALL_3")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(450, 220, 51, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setGeometry(QtCore.QRect(450, 260, 51, 31))
        self.comboBox2.setObjectName("comboBox")
        self.comboBox2.addItem("")
        self.comboBox2.setItemText(0, "")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")
        self.comboBox2.addItem("")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(510, 220, 61, 31))
        self.textEdit.setObjectName("textEdit")
        self.Add_ALL_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Add_ALL_3.setGeometry(QtCore.QRect(460, 290, 75, 23))
        self.Add_ALL_3.setObjectName("Add_ALL_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 230, 41, 21))
        self.label_4.setObjectName("label_4")
        Filter_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Filter_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 21))
        self.menubar.setObjectName("menubar")
        Filter_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Filter_Window)
        self.statusbar.setObjectName("statusbar")
        Filter_Window.setStatusBar(self.statusbar)

        self.filterdata(listWidget,all_data)
        
        

        self.Add_ALL_3.clicked.connect(self.filter_date)
        self.Apply.clicked.connect(lambda :self.filterComplete(item_head))
        self.Add_ALL_2.clicked.connect(self.select_all)
        self.Remove_ALL_3.clicked.connect(self.clear_all)
        

        self.retranslateUi(Filter_Window)
        QtCore.QMetaObject.connectSlotsByName(Filter_Window)

    def retranslateUi(self, Filter_Window):
        _translate = QtCore.QCoreApplication.translate
        Filter_Window.setWindowTitle(_translate("Filter_Window", "Date Filter"))
        self.label.setText(_translate("Filter_Window", "LIST HEADER"))
        self.Apply.setText(_translate("Filter_Window", "Apply"))
        self.Add_ALL_2.setText(_translate("Filter_Window", "Add ALL"))
        self.Remove_ALL_3.setText(_translate("Filter_Window", "Remove ALL"))
        self.comboBox.setItemText(1, _translate("Filter_Window", ">"))
        self.comboBox.setItemText(2, _translate("Filter_Window", "<"))
        self.comboBox.setItemText(3, _translate("Filter_Window", "="))
        self.comboBox2.setItemText(1, _translate("Filter_Window", "Day"))
        self.comboBox2.setItemText(2, _translate("Filter_Window", "Month"))
        self.comboBox2.setItemText(3, _translate("Filter_Window", "Year"))
        self.Add_ALL_3.setText(_translate("Filter_Window", "OK"))
        self.label_4.setText(_translate("Filter_Window", "Range"))       
        
    def filterdata(self,listWidget,all_data):
        all_data = all_data
        
        item2 = listWidget.currentItem().text()
        for i in all_data[item2].unique():
            self.item = QtWidgets.QListWidgetItem(i)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsUserCheckable)
            self.item.setCheckState(QtCore.Qt.Checked)
            self.listWidget.addItem(self.item)       

    def filter_date(self):
        op = {">":(lambda x,y:x>y),"<":(lambda x,y:x<y),"=":(lambda x,y:x==y)}        
        if self.textEdit.toPlainText() == "" or  self.comboBox.currentText() == "":
            return
        for i in range(self.listWidget.count()):
            if self.comboBox2.currentText() == "Day":
                x = self.listWidget.item(i).text()[0:2] #19-15-42
            if self.comboBox2.currentText() == "Month":
                x = self.listWidget.item(i).text()[3:5]
            if self.comboBox2.currentText() == "Year":
                x = self.listWidget.item(i).text()[6:]
            y = self.textEdit.toPlainText()
            if  op[self.comboBox.currentText()](x,y):
                self.listWidget.item(i).setCheckState(QtCore.Qt.Checked)
            else:
                self.listWidget.item(i).setCheckState(~(QtCore.Qt.Checked))
            
                
    
    def clear_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setCheckState(~(QtCore.Qt.Checked))

    def select_all(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setCheckState(QtCore.Qt.Checked)                         

    def filterComplete(self,item_head):
        self.getCheckItem = []
        self.getCheckItem.clear()
        self.item = item_head
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).checkState() != QtCore.Qt.Checked : #send Signal not check 
                self.getCheckItem.append(self.listWidget.item(i).text())

        Ui_MainWindow.getDataFilter(self,self.getCheckItem,self.item)      

class Ui_Value(object):
    def setupUi(self,item,Value):
        Value.setObjectName("Value")
        Value.resize(256, 303)
        self.centralwidget = QtWidgets.QWidget(Value)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(40, 10, 70, 17))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(40, 40, 70, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(40, 70, 70, 17))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(40, 100, 70, 17))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(40, 130, 70, 17))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(40, 160, 70, 17))
        self.checkBox_6.setObjectName("checkBox_6")
        ##Combobox
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(100, 220, 51, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 230, 51, 21))
        self.label_4.setObjectName("label_4")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(160, 220, 81, 31))
        self.textEdit.setObjectName("textEdit")        
        
        
        #Check Apply
        self.Apply = QtWidgets.QPushButton(self.centralwidget)
        self.Apply.setGeometry(QtCore.QRect(140, 80, 75, 23))
        self.Apply.setObjectName("Apply")
        self.Apply.clicked.connect(lambda :self.applyValue(item,Value))


        Value.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Value)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 268, 21))
        self.menubar.setObjectName("menubar")
        Value.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Value)
        self.statusbar.setObjectName("statusbar")
        Value.setStatusBar(self.statusbar)

        self.retranslateUi(Value)
        QtCore.QMetaObject.connectSlotsByName(Value)

        # To Check only one box!
        self.checkBox.toggled.connect(
            lambda checked: checked and self.checkBox_2.setChecked(False))
        self.checkBox.toggled.connect(
            lambda checked: checked and self.checkBox_3.setChecked(False))
        self.checkBox.toggled.connect(
            lambda checked: checked and self.checkBox_4.setChecked(False))
        self.checkBox.toggled.connect(
            lambda checked: checked and self.checkBox_5.setChecked(False))
        self.checkBox.toggled.connect(
            lambda checked: checked and self.checkBox_6.setChecked(False))   

        self.checkBox_2.toggled.connect(
            lambda checked: checked and self.checkBox.setChecked(False))
        self.checkBox_2.toggled.connect(
            lambda checked: checked and self.checkBox_3.setChecked(False))
        self.checkBox_2.toggled.connect(
            lambda checked: checked and self.checkBox_4.setChecked(False))
        self.checkBox_2.toggled.connect(
            lambda checked: checked and self.checkBox_5.setChecked(False))
        self.checkBox_2.toggled.connect(
            lambda checked: checked and self.checkBox_6.setChecked(False))   
   
        self.checkBox_3.toggled.connect(
            lambda checked: checked and self.checkBox.setChecked(False))
        self.checkBox_3.toggled.connect(
            lambda checked: checked and self.checkBox_2.setChecked(False))
        self.checkBox_3.toggled.connect(
            lambda checked: checked and self.checkBox_4.setChecked(False))
        self.checkBox_3.toggled.connect(
            lambda checked: checked and self.checkBox_5.setChecked(False))
        self.checkBox_3.toggled.connect(
            lambda checked: checked and self.checkBox_6.setChecked(False))     

        self.checkBox_4.toggled.connect(
            lambda checked: checked and self.checkBox.setChecked(False))
        self.checkBox_4.toggled.connect(
            lambda checked: checked and self.checkBox_2.setChecked(False))
        self.checkBox_4.toggled.connect(
            lambda checked: checked and self.checkBox_3.setChecked(False))
        self.checkBox_4.toggled.connect(
            lambda checked: checked and self.checkBox_5.setChecked(False))
        self.checkBox_4.toggled.connect(
            lambda checked: checked and self.checkBox_6.setChecked(False)) 

        self.checkBox_5.toggled.connect(
            lambda checked: checked and self.checkBox.setChecked(False))
        self.checkBox_5.toggled.connect(
            lambda checked: checked and self.checkBox_2.setChecked(False))
        self.checkBox_5.toggled.connect(
            lambda checked: checked and self.checkBox_3.setChecked(False))
        self.checkBox_5.toggled.connect(
            lambda checked: checked and self.checkBox_4.setChecked(False))
        self.checkBox_5.toggled.connect(
            lambda checked: checked and self.checkBox_6.setChecked(False))              

        self.checkBox_6.toggled.connect(
            lambda checked: checked and self.checkBox.setChecked(False))
        self.checkBox_6.toggled.connect(
            lambda checked: checked and self.checkBox_2.setChecked(False))
        self.checkBox_6.toggled.connect(
            lambda checked: checked and self.checkBox_3.setChecked(False))
        self.checkBox_6.toggled.connect(
            lambda checked: checked and self.checkBox_4.setChecked(False))
        self.checkBox_6.toggled.connect(
            lambda checked: checked and self.checkBox_5.setChecked(False))  

    def retranslateUi(self, Value):
        _translate = QtCore.QCoreApplication.translate
        Value.setWindowTitle(_translate("Value", " Measurement Value"))
        self.checkBox.setText(_translate("Value", "Sum"))
        self.checkBox_2.setText(_translate("Value", "Max"))
        self.checkBox_3.setText(_translate("Value", "Min"))
        self.checkBox_4.setText(_translate("Value", "Mean"))
        self.checkBox_5.setText(_translate("Value", "Median"))
        self.checkBox_6.setText(_translate("Value", "Count"))
        self.Apply.setText(_translate("Value", "Apply"))

        self.comboBox.setItemText(1, _translate("Value", ">"))
        self.comboBox.setItemText(2, _translate("Value", "<"))
        self.comboBox.setItemText(3, _translate("Value", "="))
        self.label_4.setText(_translate("Value", "Range"))
    ### Add function in here!!!!##################################

    def applyValue(self,item,Value):
        toText = self.textEdit.toPlainText()
        
        if self.checkBox.isChecked():
            print ("Sum")
            if "(" in item.text():
                op[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = "sum"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = ["",""]
                item.setText("sum("+item.text()[item.text().index("(")+1:item.text().index(")")]+")")
            else:
                op[str(item.text())] = "sum"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text())] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":                        
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text())] = ["",""] 
                item.setText("sum("+item.text()+")")
                
        elif self.checkBox_2.isChecked():
            print ("Max")         
            if "(" in item.text():
                op[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = "max"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = ["",""]
                    item.setText("max("+item.text()[item.text().index("(")+1:item.text().index(")")]+")")
                
            else:
                op[str(item.text())] = "max"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text())] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text())] = ["",""]
                item.setText("max("+item.text()+")")
                        
        elif self.checkBox_3.isChecked():
            print ("Min")
            if "(" in item.text():
                op[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = "min"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = ["",""] 
                item.setText("min("+item.text()[item.text().index("(")+1:item.text().index(")")]+")")  
                    
            else:
                op[str(item.text())] = "min"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text())] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text())] = ["",""]
                item.setText("min("+item.text()+")")
                        
        elif self.checkBox_4.isChecked():
            print ("Mean")
            if "(" in item.text():
                op[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = "mean"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = ["",""]  
                item.setText("mean("+item.text()[item.text().index("(")+1:item.text().index(")")]+")")  
                                  
            else:
                op[str(item.text())] = "mean"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text())] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text())] = ["",""]
                item.setText("mean("+item.text()+")")     

        elif self.checkBox_5.isChecked():
            print ("Median")
            if "(" in item.text():
                op[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = "median"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = ["",""]
                item.setText("median("+item.text()[item.text().index("(")+1:item.text().index(")")]+")")    

            else:
                op[str(item.text())] = "median"
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text())] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text())] = ["",""]
                item.setText("median("+item.text()+")")

        elif self.checkBox_6.isChecked():
            print ("Count")
            if "(" in item.text():
                op[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = "count"

                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text()[item.text().index("(")+1:item.text().index(")")])] = ["",""]
                item.setText("count("+item.text()[item.text().index("(")+1:item.text().index(")")]+")")
                        
            else:
                op[str(item.text())] = "count"                
                if self.comboBox.currentText() != "" and toText !="":
                    op_C[str(item.text())] = [self.comboBox.currentText(),toText]
                    print("Oprerator =", self.comboBox.currentText())
                    print("Range = ", toText)
                else:
                    if self.comboBox.currentText() == "":
                        print("No operator")
                    if toText =="":
                        print("No range Value")
                    op_C[str(item.text())] = ["",""]
                item.setText("count("+item.text()+")")       

        else:
            print("please check filterValue")

        Value.close()
    ###############################################################


class Ui_MainWindow(QtWidgets.QMainWindow,object):
    

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1107, 704)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        icon = QtGui.QIcon()
        ### Select you path of ICON
        icon.addPixmap(QtGui.QPixmap("../../../../../_งานมหาลัย/ปี 1 เทอม 2/ฟิสิก/EtIx-eki_400x400.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(380, 20, 671, 621))
        self.tabWidget.setObjectName("tabWidget")
        self.DataFrame = QtWidgets.QWidget()
        self.DataFrame.setObjectName("DataFrame")
        self.tableWidget = QtWidgets.QTableWidget(self.DataFrame)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 671, 601))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tabWidget.addTab(self.DataFrame, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 40, 671, 601))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.Grid_table_button = QtWidgets.QPushButton(self.tab)
        self.Grid_table_button.setGeometry(QtCore.QRect(300, 10, 75, 23))
        self.Grid_table_button.setObjectName("Grid_table_button")   
        self.tabWidget.addTab(self.tab, "")     
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_2.setGeometry(QtCore.QRect(50, 10, 411, 41))
        self.listWidget_2.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 41, 41))
        self.label_2.setObjectName("label_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_3.setGeometry(QtCore.QRect(50, 60, 411, 41))
        self.listWidget_3.setAutoFillBackground(False)
        self.listWidget_3.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_3.setProperty("isWrapping", False)
        self.listWidget_3.setObjectName("listWidget_3")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 31, 41))
        self.label_3.setObjectName("label_3")
        self.Plot_Bar_Button = QtWidgets.QPushButton(self.tab_3)
        self.Plot_Bar_Button.setGeometry(QtCore.QRect(570, 20, 75, 23))
        self.Plot_Bar_Button.setObjectName("Plot_Bar_Button")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 110, 641, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Plot_line_Button = QtWidgets.QPushButton(self.tab_3)
        self.Plot_line_Button.setGeometry(QtCore.QRect(570, 50, 75, 23))
        self.Plot_line_Button.setObjectName("Plot_line_Button")
        self.Plot_Pie_Button = QtWidgets.QPushButton(self.tab_3)
        self.Plot_Pie_Button.setGeometry(QtCore.QRect(570, 80, 75, 23))
        self.Plot_Pie_Button.setObjectName("Plot_Pie_Button")
        ########clear Button###########
        self.Clear_Column = QtWidgets.QPushButton(self.tab_3)
        self.Clear_Column.setGeometry(QtCore.QRect(470, 20, 75, 23))
        self.Clear_Column.setObjectName("Clear_Column")
        self.Clear_Row = QtWidgets.QPushButton(self.tab_3)
        self.Clear_Row.setGeometry(QtCore.QRect(470, 70, 75, 23))
        self.Clear_Row.setObjectName("Clear_Row")
        ######################################
        self.tabWidget.addTab(self.tab_3, "")
        self.listWidget = HeadList(self,self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(50, 90, 261, 241))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 251, 41))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.Union_Button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.Union_Button_2.setGeometry(QtCore.QRect(130, 10, 75, 23))
        self.Union_Button_2.setObjectName("Union_Button_2")
        self.listWidget_4 = HeadList(self, self.centralwidget)
        self.listWidget_4.setGeometry(QtCore.QRect(50, 380, 261, 211))
        self.listWidget_4.setObjectName("listWidget_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 70, 61, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 360, 71, 21))
        self.label_5.setObjectName("label_5")
        self.Update_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Update_Button.setGeometry(QtCore.QRect(160, 60, 75, 23))
        self.Update_Button.setObjectName("Update_Button")
        self.Default_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Default_Button.setGeometry(QtCore.QRect(240, 60, 75, 23))
        self.Default_Button.setAutoFillBackground(False)
        self.Default_Button.setCheckable(False)
        self.Default_Button.setAutoDefault(False)
        self.Default_Button.setObjectName("Default_Button")
        self.Save_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Save_Button.setGeometry(QtCore.QRect(210, 10, 75, 23))
        self.Save_Button.setObjectName("Save_button")        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1107, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True) #DRAG AND DROP
        self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)  

        self.listWidget_2.setAcceptDrops(True)
        self.listWidget_2.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)    
        self.listWidget_2.doubleClicked.connect(self.filterup)
        # self.listWidget_2.clicked.connect(self.drill_down_up)
        self.listWidget_2.installEventFilter(self)

        self.listWidget_3.setAcceptDrops(True)
        self.listWidget_3.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_3.doubleClicked.connect(self.filterdown)
        # self.listWidget_3.clicked.connect(self.drill_down_down)
        self.listWidget_3.installEventFilter(self)

        self.listWidget_4.setAcceptDrops(True)
        self.listWidget_4.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_4.setDefaultDropAction(QtCore.Qt.MoveAction) 


        self.Grid_table_button.clicked.connect(self.gridtable)
        self.pushButton.clicked.connect(self.getFile)
        self.Plot_Bar_Button.clicked.connect(self.plot_bar)
        self.Plot_line_Button.clicked.connect(self.plot_line)
        self.Default_Button.clicked.connect(self.showdata_head_backup)
        self.Save_Button.clicked.connect(self.save_head)
        self.Update_Button.clicked.connect(self.update_head)
        self.Union_Button_2.clicked.connect(self.getFile_union)
        self.Plot_Pie_Button.clicked.connect(self.plot_pie)
        self.Clear_Column.clicked.connect(self.clear_col)
        self.Clear_Row.clicked.connect(self.clear_row)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        



        self.view =WebEngineView()
        self.verticalLayout.addWidget(self.view)

        self.filter = Ui_Value()
        self.filterDimension = Ui_Filter_Window()

        self.tableWidget.setSortingEnabled(True)    

        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sianbleau"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DataFrame), _translate("MainWindow", "Data"))
        self.Grid_table_button.setText(_translate("MainWindow", "Grid Table"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Table"))
        self.label_2.setText(_translate("MainWindow", "Column"))
        self.label_3.setText(_translate("MainWindow", "Row"))
        self.Plot_Bar_Button.setText(_translate("MainWindow", "Bar Plot"))
        self.Plot_line_Button.setText(_translate("MainWindow", "Line Plot"))
        self.Plot_Pie_Button.setText(_translate("MainWindow", "Pie Plot"))
        self.Clear_Column.setText(_translate("MainWindow", "Clear"))
        self.Clear_Row.setText(_translate("MainWindow", "Clear"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Graph"))
        self.label.setText(_translate("MainWindow", "LIST HEADER"))
        self.pushButton.setText(_translate("MainWindow", "Import File"))
        self.label_4.setText(_translate("MainWindow", "Dimension"))
        self.label_5.setText(_translate("MainWindow", "Measurement "))
        self.Update_Button.setText(_translate("MainWindow", "Update"))
        self.Default_Button.setText(_translate("MainWindow", "Default"))
        self.Union_Button_2.setText(_translate("MainWindow", "Union"))
        self.Save_Button.setText(_translate("MainWindow", "Save"))

    def showdata_head(self):
        if start_ui == "0":
            return print("ERROR")
        self.listWidget.clear()
        self.listWidget_4.clear()
        global op ,filter_data,head_filter , filter_key , op_C
        filter_data = []
        head_filter = []
        op = {}
        filter_key = {}
        op_C = {}
        
        global Dimension,Measurement,Dimension_number,number,string
        Dimension = []
        Measurement = []
        Dimension_number = []
        number = []
        string = []
        Topic = headTopic()
        data_head_backup = Topic.get_backup()      
        if namefile not in data_head_backup:
            data_head_backup[namefile] = {"Dimension":[] ,"Measurement":[] }
            for x in self.all_data.columns:
                if self.all_data[x].dtypes == 'int64' or self.all_data[x].dtypes == 'float64':
                    if "ID" in x or "Code" in x or "Date" in x:
                        self.all_data[x] = self.all_data[x].astype(str)
                        Dimension.append(str(x))
                        Dimension_number.append(str(x))
                        string.append(str(x))
                        data_head_backup[namefile]["Dimension"].append(str(x))
                        self.listWidget.addItem(str(x))
                    else :
                        number.append(str(x))
                        Measurement.append(x)
                        data_head_backup[namefile]["Measurement"].append(str(x))
                        self.listWidget_4.addItem(x)
                elif self.all_data[x].dtypes == 'object':
                    Dimension.append(x)
                    string.append(str(x))
                    data_head_backup[namefile]["Dimension"].append(str(x))
                    self.listWidget.addItem(x)
                Topic.backup_head()
        else:
            for i in data_head_backup[namefile]["Dimension"]:
                self.listWidget.addItem(i)
                Dimension.append(i)
                if self.all_data[i].dtypes == 'int64' or self.all_data[i].dtypes == 'float64':
                    if "ID" in i or "Code" in i or "Date" in i:
                        string.append(str(i))
                        Dimension_number.append(str(i))
                        self.all_data[i] = self.all_data[i].astype(str)
                    else:
                        number.append(str(i))
                        self.all_data[i] = self.all_data[i].astype(str)  
                else: 
                    string.append(str(i))  
                    
            for x in data_head_backup[namefile]["Measurement"]:
                self.listWidget_4.addItem(x)
                Measurement.append(x) 
                if self.all_data[x].dtypes == 'int64' or self.all_data[x].dtypes == 'float64':
                    if "ID" in x or "Code" in x or "Date" in x:
                        Dimension_number.append(str(x))
                        string.append(str(x))                        
                    else:
                        number.append(str(x))
   
                else:
                    string.append(str(x))
                    self.all_data[x] = self.all_data[x].astype(str) 

    def split_date(self):
        Date_list = []
        split_list = []
        for i in Dimension:
            if "Date" in i:
                Date_list.append(i)
        for j in Date_list:
            split_list.append("split"+str(j))
        for x in range(len(Date_list)):
            if "-" in self.all_data[Date_list[x]][0]:
                split_list[x] = self.all_data[Date_list[x]].str.split("-",expand=True)
            if "/" in self.all_data[Date_list[x]][0]:
                split_list[x] = self.all_data[Date_list[x]].str.split("/",expand=True)
            ##### split %Y %M %D
            self.all_data[str(Date_list[x])+" Day"] = split_list[x][0]
            self.all_data[str(Date_list[x])+" Month"] = split_list[x][1]
            self.all_data[str(Date_list[x])+" Year"] = split_list[x][2]
            #### str to int
            self.all_data[str(Date_list[x])+" Day"].astype(int)
            self.all_data[str(Date_list[x])+" Month"].astype(int)
            self.all_data[str(Date_list[x])+" Year"].astype(int)
        

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.listWidget_3):
            self.index = source.currentIndex().row()
            self.menu = QtWidgets.QMenu()
            
            self.action = QtWidgets.QAction("Drill Down")
            self.action2 = QtWidgets.QAction("Delete")
            
            self.menu.addAction(self.action)
            self.menu.addAction(self.action2)

            self.action.triggered.connect(self.drill_down_down)
            self.action2.triggered.connect(lambda:self.listWidget_3.takeItem(self.index))
            if self.menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                # print(item.text())
            return True
        if (event.type() == QtCore.QEvent.ContextMenu and
            source is self.listWidget_2):
            self.index = source.currentIndex().row()
            self.menu = QtWidgets.QMenu()
            
            self.action = QtWidgets.QAction("Drill Down")
            self.action2 = QtWidgets.QAction("Delete")

            self.menu.addAction(self.action)
            self.menu.addAction(self.action2)

            self.action.triggered.connect(self.drill_down_up)
            self.action2.triggered.connect(lambda:self.listWidget_2.takeItem(self.index))
            if self.menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                # print(item.text())
            return True
        
        return super().eventFilter(source, event)


    def drill_down_up(self):
        head_columns = []
        list_widget = []
        list_widget_not_select = []
        for i in self.all_data.columns:
            head_columns.append(i)   
        
        if  "(" in self.listWidget_2.currentItem().text():
            item4 = self.listWidget_2.currentItem().text()[self.listWidget_2.currentItem().text().index("(")+1:self.listWidget_2.currentItem().text().index(")")]
        else:
            item4 = self.listWidget_2.currentItem().text()
            
        for x in  range(len(self.listWidget_2)):
            if "(" in self.listWidget_2.item(x).text():
                if self.listWidget_2.item(x).text() != item4:
                    list_widget.append(self.listWidget_2.item(x).text()[self.listWidget_2.item(x).text().index("(")+1:self.listWidget_2.item(x).text().index(")")])
                list_widget_not_select.append(self.listWidget_2.item(x).text()[self.listWidget_2.item(x).text().index("(")+1:self.listWidget_2.item(x).text().index(")")])            
            else:
                if self.listWidget_2.item(x).text() != item4:
                    list_widget.append(self.listWidget_2.item(x).text())
                list_widget_not_select.append(self.listWidget_2.item(x).text())
        if item4 in list_widget_not_select:
            if "Date" in item4:
                if "Day" in item4:
                    if head_columns[head_columns.index(item4)+1] not in list_widget: 
                        self.listWidget_2.addItem(head_columns[head_columns.index(item4[:-4]+" Month")]) 
                elif "Month" in item4:
                    if head_columns[head_columns.index(item4)+1] not in list_widget: 
                        self.listWidget_2.addItem(head_columns[head_columns.index(item4[:-6]+" Year")])     
                elif "Year" in item4:
                    pass
                else:
                    if head_columns[head_columns.index(item4)+1] not in list_widget:     
                        self.listWidget_2.addItem(head_columns[head_columns.index(item4+" Day")])
            elif item4 == head_columns[-1]:
                pass            
            else:
                if "Day" in head_columns[head_columns.index(item4)+1]:
                    pass
                else:
                    if head_columns[head_columns.index(item4)+1] not in list_widget: 
                        self.listWidget_2.addItem(head_columns[head_columns.index(item4)+1]) 
        
    def drill_down_down(self):
        head_columns = []
        list_widget = []
        list_widget_not_select = []
        for i in self.all_data.columns:
            head_columns.append(i)
        
        if  "(" in self.listWidget_3.currentItem().text():
            item4 = self.listWidget_3.currentItem().text()[self.listWidget_3.currentItem().text().index("(")+1:self.listWidget_3.currentItem().text().index(")")]
        else:
            item4 = self.listWidget_3.currentItem().text()
            
        for x in  range(len(self.listWidget_3)):
            if "(" in self.listWidget_3.item(x).text():
                if self.listWidget_3.item(x).text() != item4:
                    list_widget.append(self.listWidget_3.item(x).text()[self.listWidget_3.item(x).text().index("(")+1:self.listWidget_3.item(x).text().index(")")])
                list_widget_not_select.append(self.listWidget_3.item(x).text()[self.listWidget_3.item(x).text().index("(")+1:self.listWidget_3.item(x).text().index(")")])            
            else:
                if self.listWidget_3.item(x).text() != item4:
                    list_widget.append(self.listWidget_3.item(x).text())
                list_widget_not_select.append(self.listWidget_3.item(x).text()) 

        if item4 in list_widget_not_select:
            if "Date" in item4:
                if "Day" in item4:
                    if head_columns[head_columns.index(item4)+1] not in list_widget:    
                        self.listWidget_3.addItem(head_columns[head_columns.index(item4[-4]+" Month")]) 
                elif "Month" in item4:
                    if head_columns[head_columns.index(item4)+1] not in list_widget:
                        self.listWidget_3.addItem(head_columns[head_columns.index(item4[-6]+" Year")])     
                elif "Year" in item4:
                    pass
                else:
                    if head_columns[head_columns.index(item4)+1] not in list_widget:    
                        self.listWidget_3.addItem(head_columns[head_columns.index(item4+" Day")])
            elif item4 == head_columns[-1]:
                pass            
            else:
                if "Day" in head_columns[head_columns.index(item4)+1]:
                    pass
                else:
                    print("sad")
                    if head_columns[head_columns.index(item4)+1] not in list_widget:
                        self.listWidget_3.addItem(head_columns[head_columns.index(item4)+1]) 

    def update_head(self):
        if len(self.listWidget) == 0 and len(self.listWidget_4) == 0:
            return print("ERROR")   
        for Dimension_head in range(len(self.listWidget)):
            if "(" in self.listWidget.item(Dimension_head).text():
                self.listWidget.item(Dimension_head).setText(self.listWidget.item(Dimension_head).text()[self.listWidget.item(Dimension_head).text().index("(")+1:self.listWidget.item(Dimension_head).text().index(")")])            
            if self.listWidget.item(Dimension_head).text() not in Dimension:
                if self.listWidget.item(Dimension_head).text() in number :
                    Dimension.append(self.listWidget.item(Dimension_head).text())
                    Measurement.remove(self.listWidget.item(Dimension_head).text())
                    self.all_data[self.listWidget.item(Dimension_head).text()] = self.all_data[self.listWidget.item(Dimension_head).text()].astype(str)

                elif self.listWidget.item(Dimension_head).text() in Dimension_number :
                    Dimension.append(self.listWidget.item(Dimension_head).text())
                    Measurement.remove(self.listWidget.item(Dimension_head).text())
                    self.all_data[self.listWidget.item(Dimension_head).text()] = self.all_data[self.listWidget.item(Dimension_head).text()].astype(str) 
                
                elif  self.listWidget.item(Dimension_head).text() in string : 
                    Dimension.append(self.listWidget.item(Dimension_head).text())
                    Measurement.remove(self.listWidget.item(Dimension_head).text())         
        
        for Measurement_head in range(len(self.listWidget_4)):
            if "(" in self.listWidget_4.item(Measurement_head).text():
                self.listWidget_4.item(Measurement_head).setText(self.listWidget_4.item(Measurement_head).text()[self.listWidget_4.item(Measurement_head).text().index("(")+1:self.listWidget_4.item(Measurement_head).text().index(")")])            
            if self.listWidget_4.item(Measurement_head).text() not in Measurement:
                if  self.listWidget_4.item(Measurement_head).text() in Dimension_number:
                    Dimension.remove(self.listWidget_4.item(Measurement_head).text())
                    Measurement.append(self.listWidget_4.item(Measurement_head).text())
                    if "." in self.all_data[self.listWidget_4.item(Measurement_head).text()][0]:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(float)
                    else:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(int)
                
                elif self.listWidget_4.item(Measurement_head).text() in number:
                    Dimension.remove(self.listWidget_4.item(Measurement_head).text())
                    Measurement.append(self.listWidget_4.item(Measurement_head).text())
                    if "." in self.all_data[self.listWidget_4.item(Measurement_head).text()][0]:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(float)
                    else:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(int)                    
                
                elif  self.listWidget_4.item(Measurement_head).text() in string:
                    Dimension.remove(self.listWidget_4.item(Measurement_head).text())
                    Measurement.append(self.listWidget_4.item(Measurement_head).text())

                
    def save_head(self):
        Topic = headTopic()
        data_head_backup = Topic.get_backup() 
        del data_head_backup[namefile]["Dimension"][:]
        del data_head_backup[namefile]["Measurement"][:]       
        for i in Dimension:
            data_head_backup[namefile]["Dimension"].append(str(i)) 
        for x in Measurement:
            data_head_backup[namefile]["Measurement"].append(str(x))
        Topic.backup_head()
        
    def showdata_head_backup(self):
        if start_ui == "0":
            return print("ERROR IMPORT")
        self.listWidget.clear()
        self.listWidget_4.clear()
        Topic = headTopic()
        data_head_backup = Topic.get_backup()
        print(data_head_backup[namefile]["Dimension"],data_head_backup[namefile]["Measurement"])
        for i in data_head_backup[namefile]["Dimension"]:
            self.listWidget.addItem(i)
        for x in data_head_backup[namefile]["Measurement"]:
            self.listWidget_4.addItem(x)
            
    
    def showdata_table(self):  
        self.tableWidget.clear()
        self.split_date()
        numcolumn = len(self.all_data)
        print(len(self.all_data))
        
        if numcolumn == 0:
            numRows = len(self.all_data.index)
        else:
            numRows = numcolumn
        self.tableWidget.setColumnCount(len(self.all_data.columns))
        self.tableWidget.setRowCount(numRows)
        self.tableWidget.setHorizontalHeaderLabels(self.all_data.columns)
        for i in range(numRows):
            for j in range(len(self.all_data.columns)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.all_data.iat[i,j])))   
                    
    def readData(self):
        self.all_data = pd.read_csv(self.filename,encoding = 'windows-1252').dropna()
        global namefile
        namefile = self.filename[self.filename.index("/",-15,-1)+1:self.filename.index(".")]
        print(namefile)
        self.showdata_head()
        self.showdata_table()
        print("read file finished")

        
    def readUnionData(self):
        if self.filename == "":
            return print("ERROR IMPORT FILE")
        self.data_1 = pd.read_csv(self.filename,encoding = 'windows-1252').dropna()
        self.data_2 = pd.read_csv(self.filename_union,encoding = 'windows-1252').dropna()
        if len(self.data_1.columns) == len(self.data_2.columns):
            for i in range(len(self.data_1.columns)):
                if self.data_1.columns[i] == self.data_2.columns[i] :
                    self.all_data = pd.concat([self.data_1,self.data_2],axis=0).drop_duplicates().reset_index(drop=True)
                    self.showdata_head()
                    self.showdata_table()  
    
    def getFile(self):
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.verticalLayout.removeWidget(self.view)
        self.filename = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
        if self.filename == "" :
            print("please select file")
        else:
            global start_ui
            start_ui = "1"
            print("File :",self.filename)
            self.readData()
            

    
    def getFile_union(self):
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.verticalLayout.removeWidget(self.view)        
        if start_ui == "0":
            return print("ERROR IMPORT")
        self.filename_union = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
        if self.filename_union == "" :
            print("please select file")
        else:
            print("File :",self.filename_union)
            self.readUnionData()    
    

    def getDataFilter(self,data,item): ##recive DataFilter from filterComplete        
        filter_key[item] = data




    def data_plot(self,fig):        
        global chart
        row_index = []
        col_index = [] 
        encode_list = []
        encode_PieList = []
        encode_ColorList = []
        tooltip_list = []
        data= []
        sys.setrecursionlimit(10000)
        
        for r in range(len(self.listWidget_3)):            
            if "(" in self.listWidget_3.item(r).text() :
                row_index.append(self.listWidget_3.item(r).text()[self.listWidget_3.item(r).text().index("(")+1:self.listWidget_3.item(r).text().index(")")])
            else:
                row_index.append(self.listWidget_3.item(r).text())
        for c in range(len(self.listWidget_2)):
            if "(" in self.listWidget_2.item(c).text() :
                col_index.append(self.listWidget_2.item(c).text()[self.listWidget_2.item(c).text().index("(")+1:self.listWidget_2.item(c).text().index(")")])
            else:    
                col_index.append(self.listWidget_2.item(c).text())
        for data_row in range(len(row_index)):
            data.append(row_index[data_row])
        for data_col in range(len(col_index)):
            data.append(col_index[data_col])   
                              
        if len(col_index) >= 1 :
            if col_index[0] in Dimension:
                encode_list.append(alt.X(col_index[0]))
                tooltip_list.append(col_index[0])
                encode_PieList.append(alt.Theta(col_index[0]))
                encode_ColorList.append(alt.Color(col_index[0]))

            elif col_index[0] in Measurement:
                if col_index[0] not in op:
                    op[col_index[0]] = "sum"
                encode_list.append(alt.X(f"{op[col_index[0]]}({col_index[0]})")) 
                tooltip_list.append(f"{op[col_index[0]]}({col_index[0]})")     
                encode_PieList.append(alt.Theta(f"{op[col_index[0]]}({col_index[0]})"))
                encode_ColorList.append(alt.Color(f"{op[col_index[0]]}({col_index[0]})"))
        if len(col_index) >= 2 :
            if col_index[1] in Dimension:
                encode_list.append(alt.Column(col_index[1]))
                tooltip_list.append(col_index[1])
                

            # elif col_index[1] in Measurement:
            #     if col_index[0] in  Measurement:
            #         if col_index[1] not in op:
            #             op[col_index[1]] = "sum"
            #         encode_list.append(alt.X2(f"{op[col_index[1]]}({col_index[1]})"))
            #         tooltip_list.append(f"{op[col_index[1]]}({col_index[1]})")
                    
                                          
            else:  
                if col_index[1] not in op:
                    op[col_index[1]] = "sum"
                encode_list.append(alt.Column(f"{op[col_index[1]]}({col_index[1]})"))
                tooltip_list.append(f"{op[col_index[1]]}({col_index[1]})")    
            
        
        if len(row_index) >= 1 :
            if row_index[0] in Dimension:
                encode_list.append(alt.Y(row_index[0]))
                tooltip_list.append(row_index[0])

            elif row_index[0] in Measurement:
                if row_index[0] not in op:
                    op[row_index[0]] = "sum"
                encode_list.append(alt.Y(f"{op[row_index[0]]}({row_index[0]})"))
                tooltip_list.append(f"{op[row_index[0]]}({row_index[0]})")
        if len(row_index) >= 2 :
            if row_index[1] in Dimension:
                encode_list.append(alt.Row(row_index[1]))
                tooltip_list.append(row_index[1])

            elif row_index[1] in Measurement:
                if row_index[1] not in op:
                    op[row_index[1]] = "sum"
                encode_list.append(alt.Row(f"{op[row_index[1]]}({row_index[1]})"))
                tooltip_list.append(f"{op[row_index[1]]}({row_index[1]})")    
        
        
        if len(col_index) >= 3 or len(row_index) >= 3:
            if len(col_index) >= 3:
                if col_index[2] in Dimension:
                    encode_list.append(alt.Color(col_index[2]))
                    tooltip_list.append(col_index[2])

                elif col_index[2] in Measurement:
                    if col_index[0] in Measurement and col_index[1] in Measurement and col_index[2] in Measurement:
                        print("Error")
                        pass
                    else:
                        if col_index[2] not in op:
                            op[col_index[2]] = "sum"
                        encode_list.append(alt.Color(f"{op[col_index[2]]}({col_index[2]})"))
                        tooltip_list.append(f"{op[col_index[2]]}({col_index[2]})")     
            elif len(row_index) >= 3 :      
                if row_index[2] in Dimension:
                    encode_list.append(alt.Color(row_index[2]))
                    tooltip_list.append(row_index[2])

                elif row_index[2] in Measurement:
                    if row_index[2] not in op:
                        op[row_index[2]] = "sum"
                    encode_list.append(alt.Color(f"{op[row_index[2]]}({row_index[2]})"))
                    tooltip_list.append(f"{op[row_index[2]]}({row_index[2]})")      

        
        if fig == "bar":
            filter_str = ""
            if len(row_index) > 0 or len(col_index) > 0:
                s = row_index + col_index 
                for x in range(len(s)):
                    if s[x] not in filter_key:   
                        pass
                    else:    
                        filter_str += f"`{s[x]}` !=  {filter_key[s[x]]} and "
                for z in range(len(s)):
                    if s[z] not in op_C:   
                        pass
                    else:    
                        if op_C[s[z]][0] != "" and op_C[s[z]][0] != "":
                            filter_str += '`'+s[z]+'`' +' '+op_C[s[z]][0]+" "+op_C[s[z]][1]+" and " 
            print("OPC",op_C)                   
            print(filter_str)

            count_Row = 0
            count_Column = 0
            Alt_Axis_list = []
            col_Measure = []
            row_Measure = []
            chart_list = []
            
            #count col
            for col in col_index:
                if col in Measurement:
                    count_Column +=1
                    col_Measure.append(col)
            #count row
            for row in row_index:
                if row in Measurement:
                    count_Row += 1
                    row_Measure.append(row)
            # append data
            
            if count_Column >= 1:
                for count_col in range(count_Column) :
                    Alt_Axis_list.append(col_Measure[count_col])

            elif count_Row >= 1:
                for count_R in range(count_Row) :
                    Alt_Axis_list.append(row_Measure[count_R])            
            
            print(type(Alt_Axis_list))
            print(Alt_Axis_list)
            print(row_index)

            #meassure 2 or more

            if ((count_Column >1 and len(row_index) !=0)  or (count_Row >1 and len(col_index) !=0)):


            # 1 row Dimension Many Col Measurement
                if len(row_index) == 1 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        # min_value = min()
                        # max_value = max()
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()

                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_bar()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0]),
                            tooltip =tooltip_list)
                            
                            .resolve_scale(y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_bar()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0]),
                            tooltip =tooltip_list)
                            
                            .resolve_scale(y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0


                        
                # 1 Col Dimension Many Row Measurement
                #      
                if len(col_index) == 1 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_bar()
                            .encode(x= alt.X(col_index[0]),y= alt.Y(Alt_Axis_list[i]), tooltip =tooltip_list)
                            .resolve_scale(x="independent",y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_bar()
                            .encode(x= alt.X(col_index[0]),y= alt.Y(Alt_Axis_list[i]), tooltip =tooltip_list)
                            .resolve_scale(x="independent",y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0                


                #2 row Dimension Many Col Measurement Finish

                if len(row_index) == 2 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_bar()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='ascending')),row = alt.Row(row_index[1]),
                            tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_bar()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='ascending')),row = alt.Row(row_index[1]),
                            tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0  

                #2 col Dimension Many Row Measurement    
                        
                if len(col_index) == 2 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_bar()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_bar()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0                      
                
                #3 Row Dimension 3 Col Measurement 

                if len(row_index) == 3 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_bar()
                            .encode(x= alt.X(Alt_Axis_list[i]),y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='ascending')),row = alt.Row(row_index[1]),color= alt.Color(row_index[2]), tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_bar()
                            .encode(x = alt.X(Alt_Axis_list[i]),y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='ascending')),row = alt.Row(row_index[1]),color= alt.Color(row_index[2]), tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0  


                #3 Col Dimension 3 Measurement 

                if len(col_index) == 3 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_bar()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]),color= alt.Color(col_index[2]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_bar()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]),color= alt.Color(col_index[2]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            .properties(title="bar chart")
                            # .configure_title(anchor="start")
                            )


                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0     

            
            
            else:
                print("else")
                if filter_str != "":
                    alt.data_transformers.disable_max_rows()
                    chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                    .mark_bar()
                    .encode(*encode_list, tooltip =tooltip_list)
                    .resolve_scale(x="independent",y="independent")
                    .properties(title="bar chart")
                    .configure_title(anchor="start")
                    )    
                else:       
                    alt.data_transformers.disable_max_rows()
                    chart = (alt.Chart(self.all_data[data])
                    .mark_bar()
                    .encode(*encode_list, tooltip =tooltip_list)
                    .resolve_scale(x="independent",y="independent")
                    .properties(title="bar chart")
                    .configure_title(anchor="start")
                    )

            if ((count_Column ==1 and len(row_index) !=0)  or (count_Row ==1 and len(col_index) !=0)):
                print("if m==1")
                
                #dimension 2 Col 1  Row measurement
                if len(col_index) == 2 and row_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_bar()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_bar()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")
                        )
                #dimension 2 Row 1 Col  measurement
                if len(row_index) == 2 and col_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_bar()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_bar()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")
                        )                

                #dimension 3 Col 1  Row measurement
                if len(col_index) == 3 and row_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_bar()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]),color=alt.Color(col_index[2]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_bar()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]),color=alt.Color(col_index[2]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")
                        )
                #dimension 3 Row 1 Col  measurement
                if len(row_index) == 3 and col_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_bar()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),color=alt.Color(row_index[2]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_bar()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),color=alt.Color(row_index[2]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="bar chart")
                        # .configure_title(anchor="start")
                        ) 

        ###LINE CHART            
        elif  fig == "line":     
            filter_str = ""
            if len(row_index) > 0 or len(col_index) > 0:
                s = row_index + col_index 
                for x in range(len(s)):                    
                    if s[x] not in filter_key:   
                        pass
                    else:    
                        filter_str += f"`{s[x]}` !=  {filter_key[s[x]]} and "
                for z in range(len(s)):
                    if s[z] not in op_C:   
                        pass
                    else:    
                        if op_C[s[z]][0] != "" and op_C[s[z]][0] != "":
                            filter_str += '`'+s[z]+'`' +' '+op_C[s[z]][0]+" "+op_C[s[z]][1]+" and " 
                                                    
            count_Row = 0
            count_Column = 0
            Alt_Axis_list = []
            col_Measure = []
            row_Measure = []
            chart_list = []
            
            #count col
            for col in col_index:
                if col in Measurement:
                    count_Column +=1
                    col_Measure.append(col)
            #count row
            for row in row_index:
                if row in Measurement:
                    count_Row += 1
                    row_Measure.append(row)
            # append data
            
            if count_Column >= 1:
                for count_col in range(count_Column) :
                    Alt_Axis_list.append(col_Measure[count_col])

            elif count_Row >= 1:
                for count_R in range(count_Row) :
                    Alt_Axis_list.append(row_Measure[count_R])            
            
            print(type(Alt_Axis_list))
            print(Alt_Axis_list)
            print(row_index)

            #meassure 2 or more
            if ((count_Column >1 and len(row_index) !=0)  or (count_Row >1 and len(col_index) !=0)):
            # 1 row Dimension Many Col Measurement
            # 1 row Dimension Many Col Measurement
                if len(row_index) == 1 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):

                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()

                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array
                            .mark_line()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0]),
                            tooltip =tooltip_list)
                            
                            .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_line()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0]),
                            tooltip =tooltip_list)
                            
                            .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0


                        
                # 1 Col Dimension Many Row Measurement
                #      
                if len(col_index) == 1 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_line()
                            .encode(x= alt.X(col_index[0]),y= alt.Y(Alt_Axis_list[i]), tooltip =tooltip_list)
                            .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_line()
                            .encode(x= alt.X(col_index[0]),y= alt.Y(Alt_Axis_list[i]), tooltip =tooltip_list)
                            .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0                


                #2 row Dimension Many Col Measurement Finish

                if len(row_index) == 2 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_line()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),
                            tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            # .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_line()
                            .encode(x= alt.X(Alt_Axis_list[i]),
                            y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),
                            tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            # .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0  

                #2 col Dimension Many Row Measurement    
                        
                if len(col_index) == 2 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_line()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='descending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            # .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_line()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='descending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            # .resolve_scale(x="independent",y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0                      
                
                #3 Row Dimension 3 Col Measurement 

                if len(row_index) == 3 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_line()
                            .encode(x= alt.X(Alt_Axis_list[i]),y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),color= alt.Color(row_index[2]), tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_line()
                            .encode(x = alt.X(Alt_Axis_list[i]),y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),color= alt.Color(row_index[2]), tooltip =tooltip_list)
                            .resolve_scale(y="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0  


                #3 Col Dimension 3 Measurement 

                if len(col_index) == 3 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)):
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_line()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='descending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]),color= alt.Color(col_index[2]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")  
                            )  
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_line()
                            .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='descending')),y= alt.Y(Alt_Axis_list[i]),column = alt.Column(col_index[1]),color= alt.Color(col_index[2]), tooltip =tooltip_list)
                            .resolve_scale(x="independent")
                            .properties(title="line chart")
                            # .configure_title(anchor="start")
                            )


                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0                 
            
            else:

                if filter_str != "":
                    alt.data_transformers.disable_max_rows()
                    chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                    .mark_line()
                    .encode(*encode_list, tooltip =tooltip_list)
                    .resolve_scale(x="independent",y="independent")
                    .properties(title="line chart")
                    .configure_title(anchor="start")
                    )    
                else:       
                    alt.data_transformers.disable_max_rows()
                    chart = (alt.Chart(self.all_data[data])
                    .mark_line()
                    .encode(*encode_list, tooltip =tooltip_list)
                    .resolve_scale(x="independent",y="independent")
                    .properties(title="line chart")
                    .configure_title(anchor="start")
                    )

            if ((count_Column ==1 and len(row_index) !=0)  or (count_Row ==1 and len(col_index) !=0)):
                print("if m==1")
                
                #dimension 2 Col 1  Row measurement
                if len(col_index) == 2 and row_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_line()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_line()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")
                        )
                #dimension 2 Row 1 Col  measurement
                if len(row_index) == 2 and col_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_line()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_line()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")
                        )                

                #dimension 3 Col 1  Row measurement
                if len(col_index) == 3 and row_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_line()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]),color=alt.Color(col_index[2]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_line()
                        .encode(x= alt.X(col_index[0],sort=alt.SortField(field=col_index[0],order ='ascending')),y= alt.Y(row_index[0]),column = alt.Column(col_index[1]),color=alt.Color(col_index[2]), tooltip =tooltip_list)
                        .resolve_scale(x="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")
                        )
                #dimension 3 Row 1 Col  measurement
                if len(row_index) == 3 and col_index[0] in Measurement:
                        
                    if filter_str == "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                        .mark_line()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),color=alt.Color(row_index[2]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")  
                        )  
                        
                    else:
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_line()
                        .encode(x= alt.X(col_index[0]),
                        y= alt.Y(row_index[0],sort=alt.SortField(field=row_index[0],order ='descending')),row = alt.Row(row_index[1]),color=alt.Color(row_index[2]),tooltip =tooltip_list)
                        .resolve_scale(y="independent")
                        .properties(title="line chart")
                        # .configure_title(anchor="start")
                        ) 


        elif  fig == "pie":     
            filter_str = ""
            if len(row_index) > 0 or len(col_index) > 0:
                s = row_index + col_index 
                for x in range(len(s)):                    
                    if s[x] not in filter_key:   
                        pass
                    else:    
                        filter_str += f"`{s[x]}` !=  {filter_key[s[x]]} and "
                for z in range(len(s)):
                    if s[z] not in op_C:   
                        pass
                    else:    
                        if op_C[s[z]][0] != "" and op_C[s[z]][0] != "":
                            filter_str += '`'+s[z]+'`' +' '+op_C[s[z]][0]+" "+op_C[s[z]][1]+" and " 

            count_Row = 0
            count_Column = 0
            Alt_Axis_list = []
            col_Measure = []
            row_Measure = []
            chart_list = []
            
            #count col
            for col in col_index:
                if col in Measurement:
                    count_Column +=1
                    col_Measure.append(col)
            #count row
            for row in row_index:
                if row in Measurement:
                    count_Row += 1
                    row_Measure.append(row)
            # append data
            
            if count_Column >= 1:
                for count_col in range(count_Column) :
                    Alt_Axis_list.append(col_Measure[count_col]) #get head Item measurement

            elif count_Row >= 1:
                for count_R in range(count_Row) :
                    Alt_Axis_list.append(row_Measure[count_R])            
            
            print(type(Alt_Axis_list))
            print(Alt_Axis_list)
            print(row_index)

 

            if ((count_Column >1 and len(row_index) !=0)  or (count_Row >1 and len(col_index) !=0)):
                print("if >1")
            # 1 row Dimension Many Col Measurement
                if len(row_index) == 1 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)): 
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_arc()
                            .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")  
                            )
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_arc()
                            .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0
                
            # 1 Col Dimension Many Row Measurement
                if len(col_index) == 1 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)): 
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_arc()
                            # .encode(theta= alt.Theta(field=col_index[0],type='quantitative'),color= alt.Color(field =Alt_Axis_list[i],type='nominal'), tooltip =tooltip_list)
                            .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")  
                            )
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_arc()
                             .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.vconcat(*chart_list) # 0

            # 2 row Dimension Many Col Measurement                  

                if len(row_index) == 2 and col_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)): 
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_arc()
                            .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'),row = alt.Row(row_index[1]), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")  
                            )
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_arc()
                            .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'),row = alt.Row(row_index[1]), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart") 
                            # .configure_title(anchor="start")
                            )
                    if count_Column == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.hconcat(*chart_list) # 0

            # 2 Col Dimension Many Row Measurement
                if len(col_index) == 2 and row_index[0] in Measurement:
                    for j in range(len(Alt_Axis_list)): 
                        chart_list.append(f"chart{j}") # for chart_list have array
                    for i in range(len(Alt_Axis_list)):
                        if filter_str == "":
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data[data]) #replace chart_list array(1035)
                            .mark_arc()
                            # .encode(theta= alt.Theta(field=col_index[0],type='quantitative'),color= alt.Color(field =Alt_Axis_list[i],type='nominal'), tooltip =tooltip_list)
                            .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'),column=alt.Column(col_index[1]), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")  
                            )
                            
                        else:
                            alt.data_transformers.disable_max_rows()
                            chart_list[i] = (alt.Chart(self.all_data.query(filter_str[:-4]))
                            .mark_arc()
                             .encode(theta= alt.Theta(field =Alt_Axis_list[i],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'),column=alt.Column(col_index[1]), tooltip =tooltip_list)
                            .resolve_scale(theta="independent",color="independent")
                            .properties(title="Pie chart")
                            # .configure_title(anchor="start")
                            )
                    if count_Row == 1:
                        chart = chart_list[0]
                    else:
                        chart = alt.vconcat(*chart_list) # 0
                


            else:
                print("else")
                if filter_str != "":
                    alt.data_transformers.disable_max_rows()
                    chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                    .mark_arc()
                    .encode(*encode_PieList ,*encode_ColorList, tooltip =tooltip_list)
                    .resolve_scale(theta="independent",color="independent")
                    .properties(title="Pie chart")
                    # .configure_title(anchor="start")
                    )    
                else:       
                    alt.data_transformers.disable_max_rows()
                    chart = (alt.Chart(self.all_data[data])
                    .mark_arc()
                    .encode(*encode_PieList,*encode_ColorList , tooltip =tooltip_list)
                    .resolve_scale(theta="independent",color="independent")
                    .properties(title="Pie chart")
                    # .configure_title(anchor="start")
                    )

            if ((count_Column ==1 and len(row_index) !=0)  or (count_Row ==1 and len(col_index) !=0)):
                print("if m==1")
                if len(row_index) == 1 and col_index[0] in Measurement:
                    if filter_str != "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_arc()
                        .encode(theta= alt.Theta(field =col_index[0],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    
                    else:       
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data])
                        .mark_arc()
                        .encode(theta= alt.Theta(field =col_index[0],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )

                if len(col_index) == 1 and row_index[0] in Measurement:
                    if filter_str != "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_arc()
                        .encode(theta= alt.Theta(field =row_index[0],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    
                    else:       
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data])
                        .mark_arc()
                        .encode(theta= alt.Theta(field =row_index[0],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    

                if len(row_index) == 2 and col_index[0] in Measurement:
                    if filter_str != "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_arc()
                        .encode(theta= alt.Theta(field =col_index[0],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'),row = alt.Row(row_index[1]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    
                    else:       
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data])
                        .mark_arc()
                        .encode(theta= alt.Theta(field =col_index[0],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'),row = alt.Row(row_index[1]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )

                if len(col_index) == 2 and row_index[0] in Measurement:
                    if filter_str != "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_arc()
                        .encode(theta= alt.Theta(field =row_index[0],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    
                    else:       
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data])
                        .mark_arc()
                        .encode(theta= alt.Theta(field =row_index[0],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'),column = alt.Column(col_index[1]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )   

                if len(row_index) == 3 and col_index[0] in Measurement:
                    if filter_str != "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_arc()
                        .encode(theta= alt.Theta(field =col_index[0],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'),row = alt.Row(row_index[1] and row_index[2]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    
                    else:       
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data])
                        .mark_arc()
                        .encode(theta= alt.Theta(field =col_index[0],type='quantitative'),color= alt.Color(field=row_index[0],type='nominal'),row = alt.Row(row_index[1] and row_index[2]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )

                if len(col_index) == 3 and row_index[0] in Measurement:
                    if filter_str != "":
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data.query(filter_str[:-4]))
                        .mark_arc()
                        .encode(theta= alt.Theta(field =row_index[0],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'),column = alt.Column(col_index[1] and col_index[2]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )    
                    else:       
                        alt.data_transformers.disable_max_rows()
                        chart = (alt.Chart(self.all_data[data])
                        .mark_arc()
                        .encode(theta= alt.Theta(field =row_index[0],type='quantitative'),color= alt.Color(field=col_index[0],type='nominal'),column = alt.Column(col_index[1] and col_index[2]), tooltip =tooltip_list)
                        .resolve_scale(theta="independent",color="independent")
                        .properties(title="pie chart")
                        # .configure_title(anchor="start")
                        )   



                
    def plot_bar(self):
        print("Start Bar Plot...")
        if len(self.listWidget_3) == 0 and len(self.listWidget_2) == 0:
            return print("ERROR")   
        bar = "bar"        
        self.data_plot(bar)            
        self.verticalLayout.removeWidget(self.view)
        self.view =WebEngineView()
        self.view.updateChart(chart)
        self.verticalLayout.addWidget(self.view)
        print("Bar Plot success!!!")
        
    def plot_line(self):
        print("Start Line Plot...")
        if len(self.listWidget_3) == 0 and len(self.listWidget_2) == 0:
            return print("ERROR")   
        line = "line"
        self.data_plot(line)         
        self.verticalLayout.removeWidget(self.view)
        self.view =WebEngineView()
        self.view.updateChart(chart)
        self.verticalLayout.addWidget(self.view)
        print("Line Plot success!!!")

    def plot_pie(self):
        print("Start Pie Plot...")
        if len(self.listWidget_3) == 0 and len(self.listWidget_2) == 0:
            return print("ERROR")
        pie ="pie"
        self.data_plot(pie)            
        self.verticalLayout.removeWidget(self.view)
        self.view =WebEngineView()
        self.view.updateChart(chart)
        self.verticalLayout.addWidget(self.view)
        print("Pie Plot success!!!")       
        
    def gridtable(self):
        col_index = []
        for col in range(len(self.listWidget_2)):
            col_text = self.listWidget_2.item(col).text()
            if "(" in col_text :
                col_index.append(col_text[col_text.index("(")+1:col_text.index(")")]) 
            else:
                col_index.append(col_text)
        for row in range(len(self.listWidget_3)):
            row_text = self.listWidget_3.item(row).text()
            if "(" in row_text :
                col_index.append(row_text[row_text.index("(")+1:row_text.index(")")]) 
            else:           
                col_index.append(row_text)

                
        filter_str = ""
        if  len(col_index) > 0:
            s = col_index 
            for x in range(len(s)):               
                if s[x] not in filter_key:   
                    pass
                else:    
                    filter_str += f"`{s[x]}` !=  {filter_key[s[x]]} and "
            for z in range(len(s)):
                if s[z] not in op_C:   
                    pass
                else:
                    if op_C[s[z]][0] != "" and op_C[s[z]][0] != "":    
                        filter_str += '`'+s[z]+'`' +' '+op_C[s[z]][0]+" "+op_C[s[z]][1]+" and "      
                                        
        if filter_str != "":
            print(filter_str)
            self.tableWidget_2.setColumnCount(len(col_index))
            self.tableWidget_2.setRowCount(len(self.all_data.query(filter_str[:-4])))
            self.tableWidget_2.setHorizontalHeaderLabels(col_index)
            for i in range(len(self.all_data.query(filter_str[:-4]))):
                for j in range(len(col_index)):        
                    self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.all_data[col_index].query(filter_str[:-4]).iat[i,j]))) 
        else :
            self.tableWidget_2.setColumnCount(len(col_index))
            self.tableWidget_2.setRowCount(len(self.all_data))
            self.tableWidget_2.setHorizontalHeaderLabels(col_index)
            for i in range(len(self.all_data[col_index])):
                for j in range(len(col_index)):        
                    self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(self.all_data[col_index].iat[i,j]))) 
           

    def filterup(self):       
        item2 = self.listWidget_2.currentItem()    
        itemget = self.listWidget_2 
        if "(" in item2.text():
            if str(item2.text()[item2.text().index("(")+1:item2.text().index(")")]) in Measurement :
                self.Value = QtWidgets.QMainWindow()
                self.ui = Ui_Value()
                self.ui.setupUi(item2,self.Value)
                self.Value.show()

            else:
                if "Date" in item2.text():
                    if "Year" in item2.text() or "Month" in item2.text() or "Day" in item2.text():
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_date_Window()
                        self.ui2.setupUi(item2.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()
                    else:
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_Date_Window()
                        self.ui2.setupUi(item2.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()                                        
                else:
                    self.Filter_Window = QtWidgets.QMainWindow()
                    self.ui2 = Ui_Filter_Window()
                    self.ui2.setupUi(item2.text(),self.Filter_Window,itemget,self.all_data)
                    self.Filter_Window.show()
        else:
            if str(item2.text()) in Measurement :
                self.Value = QtWidgets.QMainWindow()
                self.ui = Ui_Value()
                self.ui.setupUi(item2,self.Value)
                self.Value.show()

            else:
                if "Date" in item2.text():
                    if "Year" in item2.text() or "Month" in item2.text() or "Day" in item2.text():
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_date_Window()
                        self.ui2.setupUi(item2.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()
                    else:
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_Date_Window()
                        self.ui2.setupUi(item2.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()                                                              
                else:                
                    self.Filter_Window = QtWidgets.QMainWindow()
                    self.ui2 = Ui_Filter_Window()
                    self.ui2.setupUi(item2.text(),self.Filter_Window,itemget,self.all_data)
                    self.Filter_Window.show()            
           

    def filterdown(self):
        item3 = self.listWidget_3.currentItem()
        itemget = self.listWidget_3
        if "(" in self.listWidget_3.currentItem().text() :  
            if str(item3.text()[item3.text().index("(")+1:item3.text().index(")")]) in Measurement :
                self.Value = QtWidgets.QMainWindow()
                self.ui = Ui_Value()
                self.ui.setupUi(item3,self.Value)
                self.Value.show()
            else :
                if "Date" in item3.text():
                    if "Year" in item3.text() or "Month" in item3.text() or "Day" in item3.text():
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_date_Window()
                        self.ui2.setupUi(item3.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()
                    else:
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_Date_Window()
                        self.ui2.setupUi(item3.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()      
                else:                                    
                    self.Filter_Window = QtWidgets.QMainWindow()
                    self.ui2 = Ui_Filter_Window()
                    self.ui2.setupUi(item3.text(),self.Filter_Window,itemget,self.all_data)
                    self.Filter_Window.show()               
        else:
            if str(item3.text()) in Measurement :
                self.Value = QtWidgets.QMainWindow()
                self.ui = Ui_Value()
                self.ui.setupUi(item3,self.Value)
                self.Value.show()
            else :
                if "Date" in item3.text():
                    if "Year" in item3.text() or "Month" in item3.text() or "Day" in item3.text():
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_date_Window()
                        self.ui2.setupUi(item3.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()
                    else:
                        self.Filter_Window = QtWidgets.QMainWindow()
                        self.ui2 = Ui_Filter_Date_Window()
                        self.ui2.setupUi(item3.text(),self.Filter_Window,itemget,self.all_data)
                        self.Filter_Window.show()  
                else:                                    
                    self.Filter_Window = QtWidgets.QMainWindow()
                    self.ui2 = Ui_Filter_Window()
                    self.ui2.setupUi(item3.text(),self.Filter_Window,itemget,self.all_data)
                    self.Filter_Window.show() 


    def clear_col(self):
        temp = []
        dimension_list = []
        measurement_list = []
        for j in range(len(self.listWidget_2)):
            if "(" in self.listWidget_2.item(j).text():
                temp.append(self.listWidget_2.item(j).text()[self.listWidget_2.item(j).text().index("(")+1:-1])
            else:
                temp.append(self.listWidget_2.item(j).text())
            
        for x in range(len(self.listWidget)):
            dimension_list.append(self.listWidget.item(x).text())
        for z in range(len(self.listWidget_4)):
            measurement_list.append(self.listWidget_4.item(z).text())

        for i in temp:
            if i not in dimension_list or i not in measurement_list :
                if "Year" in i or "Month" in i or "Day" in i :
                    pass
                else:
                    if i in Dimension:
                        if i not in dimension_list:
                            self.listWidget.addItem(i)
                    else:
                        if i not in measurement_list:
                            self.listWidget_4.addItem(i)
   
        self.listWidget_2.clear()
      
    def clear_row(self):       
        temp = []
        dimension_list = []
        measurement_list = []
        for j in range(len(self.listWidget_3)):
            if "(" in self.listWidget_3.item(j).text():
                temp.append(self.listWidget_3.item(j).text()[self.listWidget_3.item(j).text().index("(")+1:-1])
            else:
                temp.append(self.listWidget_3.item(j).text())
            
        for x in range(len(self.listWidget)):
            dimension_list.append(self.listWidget.item(x).text())
        for z in range(len(self.listWidget_4)):
            measurement_list.append(self.listWidget_4.item(z).text())

        for i in temp:
            if i not in dimension_list or i not in measurement_list :
                if "Year" in i or "Month" in i or "Day" in i :
                    pass
                else:
                    if i in Dimension:
                        if i not in dimension_list:
                            self.listWidget.addItem(i)
                    else:
                        if i not in measurement_list:
                            self.listWidget_4.addItem(i)
   
        self.listWidget_3.clear()    



if __name__ == "__main__":
    global start_ui
    start_ui = "0"
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
