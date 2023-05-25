from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDockWidget, QWidget, QPushButton
from PyQt5.QtCore import Qt
from imageWidget import ImageWidget
from tableWidget import TableWidget
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("Test Window")

        imageWidget = ImageWidget("testImages/Image.jpg")
        self.setCentralWidget(imageWidget)

        dock = QDockWidget("Tables", self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                             Qt.DockWidgetArea.RightDockWidgetArea)
        dockWidget = QWidget(dock)
        dock.setWidget(dockWidget)
        dockLayout = QVBoxLayout(dockWidget)
        dockLayout.addWidget(TableWidget("Race", ["Year", "Series", "Class"]))
        dockLayout.addWidget(TableWidget("Results", ["Placement", "Trophy"]))
        dockLayout.addWidget(TableWidget("Sailor", ["Name", "Boat"]))
        dockLayout.addWidget(QPushButton("Insert in Database"))
        

        dockWidget.setFixedSize(dockLayout.sizeHint())
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)




def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()