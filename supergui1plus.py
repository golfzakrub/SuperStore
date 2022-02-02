from logging.handlers import QueueListener
from tkinter.tix import ROW
from turtle import width
from PyQt5 import   QtCore, QtGui, QtWidgets
from matplotlib import widgets
from matplotlib.figure import Figure 
import  pandas as pd 
import sys
from PyQt5.QtWidgets import  QApplication,QTableView,QMainWindow, QTableWidgetItem,QFileDialog,QWidget
from PyQt5.QtCore import QAbstractTableModel,Qt
import numpy as np
from PyQt5.QtGui import QPainter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavigationToolbar 
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')

class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure(figsize=(30, 10))
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        super(MplWidget, self).__init__(parent)
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class AxisList(QtWidgets.QListWidget):
    def __init__(self, main, parent):
        super(AxisList, self).__init__(parent)
        self.main = main
    
    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        super().dropEvent(event)
        self.main.plot()


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        global file1
        file1 = '0'
        global file2
        file2 = '0'
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1205, 654)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(305, 30, 851, 521))
        self.tabWidget.setObjectName("tabWidget")
        self.DataFrame = QtWidgets.QWidget()
        self.DataFrame.setObjectName("DataFrame")
        self.tableWidget = QtWidgets.QTableWidget(self.DataFrame)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 850, 521))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tabWidget.addTab(self.DataFrame, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_2.setGeometry(QtCore.QRect(140, 10, 371, 41))
        self.listWidget_2.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(80, 10, 41, 41))
        self.label_2.setObjectName("label_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_3.setGeometry(QtCore.QRect(140, 60, 371, 41))
        self.listWidget_3.setAutoFillBackground(False)
        self.listWidget_3.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_3.setProperty("isWrapping", False)
        self.listWidget_3.setObjectName("listWidget_3")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(80, 70, 31, 41))
        self.label_3.setObjectName("label_3")
        self.frame = QtWidgets.QFrame(self.tab_3)
        self.frame.setGeometry(QtCore.QRect(-30, 110, 1101, 361))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 40, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 110, 521, 361))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(0, 10, 41, 41))
        self.label_4.setObjectName("label_4")
        self.listWidget_5 = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_5.setGeometry(QtCore.QRect(50, 10, 371, 41))
        self.listWidget_5.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_5.setObjectName("listWidget_5")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(0, 70, 151, 41))
        self.label_5.setObjectName("label_5")
        self.listWidget_6 = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_6.setGeometry(QtCore.QRect(50, 60, 371, 41))
        self.listWidget_6.setFlow(QtWidgets.QListView.LeftToRight)
        self.listWidget_6.setObjectName("listWidget_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(440, 40, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 261, 241))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 251, 41))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.listWidget_4 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_4.setGeometry(QtCore.QRect(20, 341, 261, 211))
        self.listWidget_4.setObjectName("listWidget_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1005, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(550, 550, 201, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")


        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(285, 200, 20, 200))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragEnabled(True) #DRAG AND DROP
        self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)  

        self.listWidget_2.setAcceptDrops(True)
        self.listWidget_2.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)    

        self.listWidget_3.setAcceptDrops(True)
        self.listWidget_3.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_3.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.listWidget_4.setAcceptDrops(True)
        self.listWidget_4.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_4.setDefaultDropAction(QtCore.Qt.MoveAction)    

        self.listWidget_5.setAcceptDrops(True)
        self.listWidget_5.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_5.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.listWidget_6.setAcceptDrops(True)
        self.listWidget_6.setDragEnabled(True) #DRAG AND DROP
        self.listWidget_6.setDefaultDropAction(QtCore.Qt.MoveAction)

        self.pushButton.clicked.connect(self.getFile)
        self.plotWidget = MplWidget(self.frame)
        self.plotWidget.setGeometry(QtCore.QRect(100,-30, 830,  420))
        self.plotWidget.setObjectName("plotWidget")


   
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DataFrame), _translate("MainWindow", "Tab 1"))
        self.label_2.setText(_translate("MainWindow", "Column"))
        self.label_3.setText(_translate("MainWindow", "Row"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Page"))
        self.label_4.setText(_translate("MainWindow", "Column"))
        self.label_5.setText(_translate("MainWindow", "Row"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.label.setText(_translate("MainWindow", "LIST HEADER"))
        self.pushButton.setText(_translate("MainWindow", "Import File"))
        self.tableWidget.setSortingEnabled(True)
        self.pushButton_2.clicked.connect(self.graph)



    def showdata_head(self):
        global Dimension,Measurement
        Dimension = []
        Measurement = []
        for x in self.all_data.columns:
            if self.all_data[x].dtypes == 'int64' or self.all_data[x].dtypes == 'float64':
                if "ID" in x or "Code" in x or "Date" in x:
                    Dimension.append(x)
                    self.listWidget.addItem(x)
                else :
                    Measurement.append(x)
                    self.listWidget_4.addItem(x)
            elif self.all_data[x].dtypes == 'object':
                Dimension.append(x)
                self.listWidget.addItem(x)

    def showdata_table(self):
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
        # self.all_data = pd.read_csv(self.filename,encoding = "utf-8").fillna(0)

        self.all_data = pd.read_csv(self.filename,encoding = 'windows-1252').fillna(0)
        self.showdata_head()
        # self.showdata_table()
    
    def  getFile(self):
        self.filename = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
        if self.filename == "" :
            print("please select file")
        else:
            print("File :",self.filename)
            self.readData()

    # def readData(self):
    #     print("read data")

    #     if self.getFile() == 1:
    #         print("read gettttttttt")
            
    #         self.all_data = pd.read_csv(self.filename,encoding = 'windows-1252').fillna(0)
    #         self.showdata_head()
    #         # self.showdata_table()

    #     if self.get_union() == 1: 
    #         print("read get_union")
    #         self.data_1 = pd.read_csv(self.filename,encoding = 'windows-1252').fillna(0)
    #         self.data_2 = pd.read_csv(self.filename_union,encoding = 'windows-1252').fillna(0)
    #         self.all_data = pd.concat([self.data_1,self.data_2],axis=0).drop_duplicates().reset_index(drop=True)
    #         self.showdata_head()
    #         # self.showdata_table()    

    
    # def getFile(self):
    #     print("getfile ceheck")
    #     self.filename = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
    #     if self.filename == "" :
    #         print("please select file")
    #     else:
    #         print("File :",self.filename)
    #         self.readData()
    #         file1 = "1"
    
    # def get_union(self):
    #     print("getfile union check")
    #     self.filename_union = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
    #     if self.filename_union == "" :
    #         print("please select file")
    #     else:
    #         print("File :",self.filename_union)
    #         self.readData()
    #         file2 = "1"


    def setupSliderX(self):
        self.lims = np.array(self.plotWidget.canvas.ax.get_xlim())
        # self.lims = np.array(self.plotWidget.canvas.ax.get_ylim())
        self.horizontalScrollBar.actionTriggered.connect(self.updatex)
        # self.verticalScrollBar.actionTriggered.connect(self.updatey)
        self.updatex()


    def setupSliderY(self):
        # self.lims = np.array(self.plotWidget.canvas.ax.get_xlim())
        self.lims = np.array(self.plotWidget.canvas.ax.get_ylim())
        # self.horizontalScrollBar.actionTriggered.connect(self.updatex)
        self.verticalScrollBar.actionTriggered.connect(self.updatey)
        self.updatey()

    def updatex(self, evt=None):
        r = self.horizontalScrollBar.value() / ((1 + self.step) *100 )
        l1 = self.lims[0] + r * np.diff(self.lims)
        l2 = l1 + np.diff(self.lims) * self.step
        self.plotWidget.canvas.ax.set_xlim(l1, l2)
        self.plotWidget.canvas.draw_idle()

    def updatey(self, evt=None):
        r = self.verticalScrollBar.value() / ((1 + self.step) *100 )
        l3 = self.lims[0] + r * np.diff(self.lims)
        l4 = l3 + np.diff(self.lims) * self.step
        self.plotWidget.canvas.ax.set_ylim(l3, l4)
        self.plotWidget.canvas.draw_idle()
   
    # def setupSlider(self):
    #     self.lims = np.array(self.plotWidget.canvas.ax.get_xlim())
    #     self.horizontalScrollBar.actionTriggered.connect(self.update)
    #     self.update()

    # def update(self, evt=None):
    #     r = self.horizontalScrollBar.value() / ((1 + self.step) * 100)
    #     l1 = self.lims[0] + r * np.diff(self.lims)
    #     l2 = l1 + np.diff(self.lims) * self.step
    #     self.QtWidget.plotWidget.canvas.ax.set_xlim(l1, l2)
    #     self.QtWidget.plotWidget.canvas.draw_idle()
    
    def graph(self): ## ยังไม่ได้แยกอันที่มี measurement ของอัน 
        row_index = []
        col_index = []
        for r in range(len(self.listWidget_3)):
            row_index.append(self.listWidget_3.item(r).text())
            for c in range(len(self.listWidget_2)):
                col_index.append(self.listWidget_2.item(0).text())        
                if row_index[r] != "" or col_index[c] !="":                           
                    datarow = []
                    datacol = [] 
                    data = self.all_data
                    if row_index[r] in Dimension:
                        if col_index[c] in Measurement:
                            for i in range(len(data.groupby([row_index[r]],as_index=False).sum()[col_index[c]])):
                                datacol.append(data.groupby([row_index[r]],as_index=False).sum()[col_index[c]][i])
                            for i2 in data[row_index[r]]:
                                if type(i2) == int or type(i2) == float:                                    
                                    if i2 not in datarow:
                                        datarow.append(str(i2)) 
                                else:
                                    if i2 not in datarow:
                                        datarow.append(i2) 
                        # print(datarow)
                        # print(datacol)
                        print(len(datarow))
                        print(len(datacol))   
                        plt.bar(datarow,datacol)
                        plt.title("Graph ")
                        plt.show()


                        self.step = 5/len(datarow)
                        self.plotWidget.canvas.ax.clear()
                        self.plotWidget.canvas.ax.bar(datarow, datacol, width=0.8, align='center')
                        self.plotWidget.canvas.ax.autoscale()
                        self.plotWidget.canvas.ax.set_xticks(range(0, len(datarow), 1))
                        self.plotWidget.canvas.draw()
                        self.setupSliderX()
                        
                        # self.update()   
                        
                    if col_index[c] in Dimension:
                        if row_index[r] in Measurement:
                            for i3 in range(len(data.groupby([col_index[c]],as_index=False).sum()[row_index[r]])):
                                datarow.append(data.groupby([col_index[c]],as_index=False).sum()[row_index[r]][i3])
                                
                            for i4 in data[col_index[c]]:
                                if type(i4) == int or type(i4) == float:
                                    if str(i4) not in datacol:
                                        datacol.append(str(i4))                                        
                                else:
                                    if i4 not in datacol:
                                        datacol.append(i4)
                            
                        # print(type(i4))
                        # print(datarow)
                        # print(datacol)   
                        plt.barh(datacol,datarow)
                        plt.title("Graph ")
                        plt.show()


                        self.step = 5/len(datacol)
                        self.plotWidget.canvas.ax.clear()
                        self.plotWidget.canvas.ax.barh(datacol, datarow, align='center')
                        self.plotWidget.canvas.ax.autoscale()
                        self.plotWidget.canvas.ax.set_yticks(range(0, len(datacol), 1))         
                        self.plotWidget.canvas.draw()
                        
                        self.setupSliderY()
                        


                else:
                    print("ERROR")

            
            
            
    # def update(self):
    
    #     self.plotWidget.ax.cla()  # clear the axes content

    #     self.plotWidget.canvas.draw_idle()  # actually draw the new content
    #         # self.setupSlider()
    #         # self.plotWidget.canvas.ax.tick_params(axis='x', rotation=10)        

            



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
    
    
    