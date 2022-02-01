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
 
 
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1005, 654)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(400, 30, 541, 521))
        self.tabWidget.setObjectName("tabWidget")
        self.DataFrame = QtWidgets.QWidget()
        self.DataFrame.setObjectName("DataFrame")
        self.tableWidget = QtWidgets.QTableWidget(self.DataFrame)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 541, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tabWidget.addTab(self.DataFrame, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_2.setGeometry(QtCore.QRect(50, 10, 121, 41))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 41, 41))
        self.label_2.setObjectName("label_2")
        self.listWidget_3 = QtWidgets.QListWidget(self.tab_3)
        self.listWidget_3.setGeometry(QtCore.QRect(50, 60, 121, 41))
        self.listWidget_3.setObjectName("listWidget_3")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(0, 70, 31, 41))
        self.label_3.setObjectName("label_3")
        self.frame = QtWidgets.QFrame(self.tab_3)
        self.frame.setGeometry(QtCore.QRect(10, 110, 521, 361))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 40, 75, 23))
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
        self.listWidget_5.setGeometry(QtCore.QRect(50, 10, 121, 41))
        self.listWidget_5.setObjectName("listWidget_5")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(0, 70, 151, 41))
        self.label_5.setObjectName("label_5")
        self.listWidget_6 = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_6.setGeometry(QtCore.QRect(50, 60, 121, 41))
        self.listWidget_6.setObjectName("listWidget_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(180, 40, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(50, 70, 261, 241))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 251, 41))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.listWidget_4 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_4.setGeometry(QtCore.QRect(50, 341, 261, 211))
        self.listWidget_4.setObjectName("listWidget_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1005, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

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
        self.plotWidget.setGeometry(QtCore.QRect(0,0, 450,  350))
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

        
    # def graph(self):
    #     row = self.listWidget_3.item(0).text()
    #     col =self.listWidget_2.item(0).text()
    #     if row == "" or col == "":
    #         print("error")
    #     else:                           
    #         datarow = []
    #         datacol = []
    #         if "ID" in row or "Code" in row or "Date" in row:
    #             pass
    #         else:
    #             for i in self.all_data[row]:
    #                 datarow.append(i)
                
    #         if "ID" in col or "Code" in col or "Date" in col:
    #             pass
    #         else:
    #             for i in self.all_data[col]:
    #                 datacol.append(i)
                    

    #         self.figure = plt.figure()

    #         self.figure.clear()
    #         ax = self.figure.subplot(figsize=(5, 5), dpi=100)      
            
    #         ax.hold(False)  
            
    #         ax.axes.bar(datarow,datacol)
    #         ax.axes.set(xlabel=row,ylabel=col,title="Graph")
    #         self.draw()
            
    #         self.setCentralWidget(self.widget)
            
    def plot(self):
        row = self.listWidget_3.item(0).text()
        col =self.listWidget_2.item(0).text()
        if row == "" or col == "":
            print("error")
        else:                           
            datarow = []
            datacol = []
            if "ID" in row or "Code" in row or "Date" in row:
                pass
            else:
                for i in self.all_data[row]:
                    datarow.append(i)
                
            if "ID" in col or "Code" in col or "Date" in col:
                pass
            else:
                for i in self.all_data[col]:
                    datacol.append(i)
                    
            y = self.all_data[col]
            x = self.all_data[row]
            # sc = MplCanvas(self, width=5, height=4, dpi=100)

    #         self.step = 5/len(x)
    #         self.QtWidget.plotWidget.canvas.ax.bar(x, y, width=0.8, align='center')
    #         self.QtWidget.plotWidget.canvas.ax.autoscale()
    #         self.QtWidget.plotWidget.canvas.ax.set_xticks(range(0, len(x), 1))
    #         self.QtWidget.plotWidget.canvas.draw()
    #         self.setupSlider()
    #         # self.plotWidget.canvas.ax.tick_params(axis='x', rotation=10)
    
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
    
    def graph(self):
        row = self.listWidget_3.item(0).text()
        col =self.listWidget_2.item(0).text()
 
        if row != "" or col !="":                           
            datarow = []
            datacol = [] 
            data = self.all_data
            # print(data.groupby([row],as_index=False).sum()[row][0])             
            # print(type(data.groupby([row],as_index=False).sum()[row][0]))                    
            # if data.groupby([col],as_index=False).sum()[row][0] == 'numpy.int64' or data.groupby([col],as_index=False).sum()[row][0] == 'numpy.float64':
            #     if "ID" in row or "Code" in row or "Date" in row:
            #         pass
            #     else:
            #         print("1")
            #         for i in range(len(data.groupby([col],as_index=False).sum()[row])):
            #             datarow.append(data.groupby([col],as_index=False).sum()[row][i]) 
            #         print("2")                           
            #         for i1 in data.groupby([col],as_index=False).sum()[col]:
            #             if i1 not in datacol:
            #                 datacol.append(i1) 
            #         print("4")
            # elif  data.groupby([col],as_index=False).sum()[row][0] != 'numpy.int64' or data.groupby([col],as_index=False).sum()[row][0] != 'numpy.float64':
            #     if "ID" in col or "Code" in col or "Date" in col:
            #         pass
            #     else:
            #         for i2 in range(len(data.groupby([row],as_index=False).sum()[row])):
            #             datacol.append(data.groupby([row],as_index=False).sum()[row][i2])
                        
            #         for i3 in data.groupby([col],as_index=False).sum()[row]:
            #             if i3 not in datarow:
            #                 datarow.append(i3)   
                            
            # print("row",type(data[row][0]),data[row][0])
            # print("col",type(data[col][0]),data[col][0])                
            # print(data.groupby([row],as_index=False).sum()[col])
            # print(data.groupby([col],as_index=False).sum()[row])                  
            # if (type(data[row][0]) == str and (type(data[col][0]) == int or type(data[col][0]) == float)):
            #     for i in range(len(data.groupby([row],as_index=False).sum()[col])):
            #         datacol.append(data.groupby([row],as_index=False).sum()[col][i])
            #     for i2 in data[row]:
            #         if i2 not in datarow:
            #             datarow.append(i2)
                        
            # if (type((data[row][0]) == int or type(data[row][0]) == float) and type(data[col][0]) == str):
            #     for i3 in range(len(data.groupby([col],as_index=False).sum()[row])):
            #         datarow.append(data.groupby([col],as_index=False).sum()[row][i3])
                    
            #     for i4 in data[col]:
            #         if i4 not in datacol:
            #             datacol.append(i4)
                        
            if row in Dimension:
                if col in Measurement:
                    for i in range(len(data.groupby([row],as_index=False).sum()[col])):
                        datacol.append(data.groupby([row],as_index=False).sum()[col][i])
                    for i2 in data[row]:
                        if i2 not in datarow:
                            datarow.append(i2) 
                print(datarow)
                print(datacol)   
                plt.bar(datarow,datacol)
                plt.title("Graph ")
                plt.show()

                self.step = 5/len(datarow)
                self.plotWidget.canvas.ax.bar(datarow, datacol, width=0.8, align='center')
                self.plotWidget.canvas.ax.autoscale()
                self.plotWidget.canvas.ax.set_xticks(range(0, len(datarow), 1))
                self.plotWidget.canvas.draw()
                # self.update()   
                 
            if col in Dimension:
                if row in Measurement:
                    for i3 in range(len(data.groupby([col],as_index=False).sum()[row])):
                        datarow.append(data.groupby([col],as_index=False).sum()[row][i3])
                        
                    for i4 in data[col]:
                        if i4 not in datacol:
                            datacol.append(i4)
                    

                print(datarow)
                print(datacol)   
                plt.barh(datacol,datarow)
                plt.title("Graph ")
                plt.show()

                self.step = 5/len(datacol)
                self.plotWidget.canvas.ax.barh(datacol, datarow, align='center')
                self.plotWidget.canvas.ax.autoscale()
                self.plotWidget.canvas.ax.set_yticks(range(0, len(datacol), 1))         
                self.plotWidget.canvas.draw()
                # self.plotWidget.ax.cla()
                # self.plotWidget.canvas.draw_idle()
                # # self.update()
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
    
    
    