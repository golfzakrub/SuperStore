#pyuic5 -x gui.ui -o guitest2.py

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import  QApplication,QTableView,QMainWindow, QTableWidgetItem,QFileDialog,QWidget
import  pandas as pd
from io import StringIO
import altair as alt


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


class Ui_Value(object):
    def setupUi(self,item,Value):
        Value.setObjectName("Value")
        Value.resize(268, 225)
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
        Value.setWindowTitle(_translate("Value", "MainWindow"))
        self.checkBox.setText(_translate("Value", "Sum"))
        self.checkBox_2.setText(_translate("Value", "Max"))
        self.checkBox_3.setText(_translate("Value", "Min"))
        self.checkBox_4.setText(_translate("Value", "Mean"))
        self.checkBox_5.setText(_translate("Value", "Median"))
        self.checkBox_6.setText(_translate("Value", "Count"))
        self.Apply.setText(_translate("Value", "Apply"))

    ### Add function in here!!!!##################################
    def applyValue(self,item,Value):
        if self.checkBox.isChecked():
            print ("Sum")
            op[str(item)] = "sum"
            Value.destroy()
        elif self.checkBox_2.isChecked():
            print ("Max")
            op[str(item)] = "max"
            Value.destroy()
        elif self.checkBox_3.isChecked():
            print ("Min")
            op[str(item)] = "min"
            Value.destroy()
        elif self.checkBox_4.isChecked():
            print ("Mean")
            op[str(item)] = "mean"
            Value.destroy()
        elif self.checkBox_5.isChecked():
            print ("Median")
            op[str(item)] = "median"
            Value.destroy()
        elif self.checkBox_6.isChecked():
            print ("Count")
            op[str(item)] = "count"
            Value.destroy()

        else:
            print("please select filterValue")
    ###############################################################

class Ui_MainWindow(object):
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
        self.tabWidget.addTab(self.tab_3, "")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
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
        self.listWidget_4 = QtWidgets.QListWidget(self.centralwidget)
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

        self.listWidget_3.setAcceptDrops(True)
        self.listWidget_3.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_3.doubleClicked.connect(self.filterdown)
      
        self.listWidget_4.setAcceptDrops(True)
        self.listWidget_4.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_4.setDefaultDropAction(QtCore.Qt.MoveAction)    
        
        self.pushButton.clicked.connect(self.getFile)
        self.Plot_Bar_Button.clicked.connect(self.plot_bar)
        self.Plot_line_Button.clicked.connect(self.plot_line)
        self.Default_Button.clicked.connect(self.showdata_head)
        self.Update_Button.clicked.connect(self.update_head)
        self.Union_Button_2.clicked.connect(self.getFile_union)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.view =WebEngineView()
        self.verticalLayout.addWidget(self.view)

        self.filter = Ui_Value()

        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sianbleau"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DataFrame), _translate("MainWindow", "Data"))
        self.label_2.setText(_translate("MainWindow", "Column"))
        self.label_3.setText(_translate("MainWindow", "Row"))
        self.Plot_Bar_Button.setText(_translate("MainWindow", "Bar Plot"))
        self.Plot_line_Button.setText(_translate("MainWindow", "Line Plot"))
        self.Plot_Pie_Button.setText(_translate("MainWindow", "Pie Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Graph"))
        self.label.setText(_translate("MainWindow", "LIST HEADER"))
        self.pushButton.setText(_translate("MainWindow", "Import File"))
        self.label_4.setText(_translate("MainWindow", "Dimension"))
        self.label_5.setText(_translate("MainWindow", "Measurement "))
        self.Update_Button.setText(_translate("MainWindow", "Update"))
        self.Default_Button.setText(_translate("MainWindow", "Default"))
        self.Union_Button_2.setText(_translate("MainWindow", "Union"))
        
    def showdata_head(self):
        self.listWidget.clear()
        self.listWidget_4.clear()
        global op
        op = {}
        global Dimension,Measurement,Dimension_backup,Measurement_backup,Dimension_number
        Dimension = []
        Measurement = []
        Dimension_number = []
        Dimension_backup = []
        Measurement_backup = []
        for x in self.all_data.columns:
            if self.all_data[x].dtypes == 'int64' or self.all_data[x].dtypes == 'float64':
                if "ID" in x or "Code" in x or "Date" in x:
                    self.all_data[x] = self.all_data[x].astype(str)
                    Dimension.append(str(x))
                    Dimension_number.append(str(x))
                    Dimension_backup.append(str(x))
                    self.listWidget.addItem(str(x))
                else :
                    Measurement.append(x)
                    Measurement_backup.append(x)
                    self.listWidget_4.addItem(x)
            elif self.all_data[x].dtypes == 'object':
                Dimension.append(x)
                Dimension_backup.append(str(x))
                self.listWidget.addItem(x)
        
    def update_head(self):
        print(Dimension,Measurement,Dimension_backup,Measurement_backup)
        for Dimension_head in range(len(self.listWidget)):
            if self.listWidget.item(Dimension_head).text() not in Dimension:
                if self.listWidget.item(Dimension_head).text() in Measurement_backup :
                    Dimension.append(self.listWidget.item(Dimension_head).text())
                    print(Dimension_head)
                    print(self.listWidget.item(Dimension_head).text())
                    Measurement.remove(self.listWidget.item(Dimension_head).text())
                    self.all_data[self.listWidget.item(Dimension_head).text()] = self.all_data[self.listWidget.item(Dimension_head).text()].astype(str)

                elif self.listWidget.item(Dimension_head).text() in Dimension_number :
                    Dimension.append(self.listWidget.item(Dimension_head).text())
                    print(Dimension_head)
                    print(self.listWidget.item(Dimension_head).text())
                    Measurement.remove(self.listWidget.item(Dimension_head).text())
                    self.all_data[self.listWidget.item(Dimension_head).text()] = self.all_data[self.listWidget.item(Dimension_head).text()].astype(str)            
        
        for Measurement_head in range(len(self.listWidget_4)):
            if self.listWidget_4.item(Measurement_head).text() not in Measurement:
                if  self.listWidget_4.item(Measurement_head).text() in Dimension_number:
                    Dimension.remove(self.listWidget_4.item(Measurement_head).text())
                    Measurement.append(self.listWidget_4.item(Measurement_head).text())
                    if "." in self.all_data[self.listWidget_4.item(Measurement_head).text()][0]:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(float)
                    else:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(int)
                
                elif self.listWidget_4.item(Measurement_head).text() in Measurement_backup:
                    Dimension.remove(self.listWidget_4.item(Measurement_head).text())
                    Measurement.append(self.listWidget_4.item(Measurement_head).text())
                    if "." in self.all_data[self.listWidget_4.item(Measurement_head).text()][0]:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(float)
                    else:
                        self.all_data[self.listWidget_4.item(Measurement_head).text()] = self.all_data[self.listWidget_4.item(Measurement_head).text()].astype(int)                    
    
    
    def showdata_table(self):
        self.tableWidget.clear()
        numcolumn = len(self.all_data)
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
        self.all_data = pd.read_csv(self.filename,encoding = 'windows-1252').fillna(0)
        self.showdata_head()
        self.showdata_table()
        
    def readUnionData(self):
        self.data_1 = pd.read_csv(self.filename,encoding = 'windows-1252').fillna(0)
        self.data_2 = pd.read_csv(self.filename_union,encoding = 'windows-1252').fillna(0)
        if len(self.data_1.columns) == len(self.data_2.columns):
            for i in range(len(self.data_1.columns)):
                if self.data_1.columns[i] == self.data_2.columns[i] :
                    self.all_data = pd.concat([self.data_1,self.data_2],axis=0).drop_duplicates().reset_index(drop=True)
                    self.showdata_head()
                    self.showdata_table()  
    
    def getFile(self):
        self.filename = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
        if self.filename == "" :
            print("please select file")
        else:
            print("File :",self.filename)
            self.readData()

    
    def getFile_union(self):
        self.filename_union = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
        if self.filename_union == "" :
            print("please select file")
        else:
            print("File :",self.filename_union)
            self.readUnionData()    
    
    def data_plot(self,fig):
        global chart
        row_index = []
        col_index = []
        encode_list = []
        tooltip_list = []
        data = []
        filter_data = []
        head_filter = []
        for r in range(len(self.listWidget_3)):
            row_index.append(self.listWidget_3.item(r).text())
        for c in range(len(self.listWidget_2)):
            col_index.append(self.listWidget_2.item(c).text())
        for data_row in range(len(row_index)):
            data.append(row_index[data_row])
        for data_col in range(len(col_index)):
            data.append(col_index[data_col])   
            
        if len(col_index) >= 1 :
            if col_index[0] in Dimension:
                encode_list.append(alt.X(col_index[0]))
                tooltip_list.append(col_index[0])

            elif col_index[0] in Measurement:
                encode_list.append(alt.X(f"{op[col_index[0]]}({col_index[0]})")) ## sum(City)
                tooltip_list.append(f"{op[col_index[0]]}({col_index[0]})")     
        
        if len(col_index) >= 2 :
            if col_index[1] in Dimension:
                encode_list.append(alt.Column(col_index[1]))
                tooltip_list.append(col_index[1])

            elif col_index[0] in Measurement:
                encode_list.append(alt.Column(f"{op[col_index[1]]}({col_index[1]})"))
                tooltip_list.append(f"{op[col_index[1]]}({col_index[1]})")    
            
        
        if len(row_index) >= 1 :
            if row_index[0] in Dimension:
                encode_list.append(alt.Y(row_index[0]))
                tooltip_list.append(row_index[0])

            elif row_index[0] in Measurement:
                encode_list.append(alt.Y(f"{op[row_index[0]]}({row_index[0]})"))
                tooltip_list.append(f"{op[row_index[0]]}({row_index[0]})")
        if len(row_index) >= 2 :
            if row_index[1] in Dimension:
                encode_list.append(alt.Row(row_index[1]))
                tooltip_list.append(row_index[1])

            elif row_index[1] in Measurement:
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
                        encode_list.append(alt.Color(f"{op[col_index[2]]}({col_index[2]})"))
                        tooltip_list.append(f"{op[col_index[2]]}({col_index[2]})")     
            elif len(row_index) >= 3 :      
                if row_index[2] in Dimension:
                    encode_list.append(alt.Color(row_index[2]))
                    tooltip_list.append(row_index[2])

                elif row_index[2] in Measurement:
                    encode_list.append(alt.Color(f"{op[row_index[2]]}({row_index[2]})"))
                    tooltip_list.append(f"{op[row_index[2]]}({row_index[2]})")      

        
        if fig == "bar":
            filter_str = ""
            if len(filter_data) > 0:
                for j in head_filter: 
                    for i in filter_data:
                        if i == filter_data[(len(filter_data)-1)]:
                            filter_str += head_filter[j] +' != "'+i+'"' ' " '
                        else:
                            filter_str += head_filter[j] +' != "'+i+'"' +" and "
            
                alt.data_transformers.disable_max_rows()
                chart = (alt.Chart(self.all_data.query(filter_str))
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
                .properties(title="line chart")
                .configure_title(anchor="start")
                ) 
        elif  fig == "line":     
            filter_str = ""
            if len(filter_data) > 0:
                for j in head_filter: 
                    for i in filter_data:
                        if i == filter_data[(len(filter_data)-1)]:
                            filter_str += head_filter[j] +' != "'+i+'"' ' " '
                        else:
                            filter_str += head_filter[j] +' != "'+i+'"' +" and "
            
                alt.data_transformers.disable_max_rows()
                chart = (alt.Chart(self.all_data.query(filter_str))
                .mark_line()
                .encode(*encode_list, tooltip =tooltip_list)
                .resolve_scale(x="independent",y="independent")
                .properties(title="bar chart")
                .configure_title(anchor="start")
                )    
            else:       
                alt.data_transformers.disable_max_rows()

                chart = (alt.Chart(self.all_data[data])
                .mark_line()
                .encode(*encode_list, tooltip =tooltip_list)
                .resolve_scale(x="independent",y="independent")
                .properties(title="bar chart")
                .configure_title(anchor="start")
                ) 
                
    def plot_bar(self): 
        bar = "bar"        
        self.data_plot(bar)            
        self.verticalLayout.removeWidget(self.view)
        self.view =WebEngineView()
        self.view.updateChart(chart)
        self.verticalLayout.addWidget(self.view)
        
    def plot_line(self):
        line = "line"
        self.data_plot(line)         
        self.verticalLayout.removeWidget(self.view)
        self.view =WebEngineView()
        self.view.updateChart(chart)
        self.verticalLayout.addWidget(self.view)
        


    def filterup(self):
        item2 = self.listWidget_2.currentItem()     
        if str(item2.text()) in Measurement :
            self.Value = QtWidgets.QMainWindow()
            self.ui = Ui_Value()
            self.ui.setupUi(item2.text(),self.Value)
            self.Value.show()
        else :
            print("Not Measurement")



    def filterdown(self):
        item3 = self.listWidget_3.currentItem()
        if str(item3.text()) in Measurement :
            self.Value = QtWidgets.QMainWindow()
            self.ui = Ui_Value()
            self.ui.setupUi(item3.text(),self.Value)
            self.Value.show()
        else :
            print("Not Measurement")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

