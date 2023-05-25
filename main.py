from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt
from imageWidget import ImageWidget
from tableWidget import TableWidget
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.move(200, 100)
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("Test Window")

        self.imageWidget = ImageWidget("testImages/Image.jpg")
        self.setCentralWidget(self.imageWidget)

        dock = QDockWidget(self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.tables = QWidget(dock)
        dock.setWidget(self.tables)
        tableLayout = QVBoxLayout(self.tables)

        tableLayout.addWidget(TableWidget("Race", ["Year", "Series", "Class"]))
        tableLayout.addWidget(TableWidget("Results", ["Placement", "Trophy"]))
        tableLayout.addWidget(TableWidget("Sailor", ["Name", "Boat"]))
        tableLayout.addWidget(QPushButton("Insert in Database"))
        

        self.tables.setFixedSize(tableLayout.sizeHint())
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)




def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()