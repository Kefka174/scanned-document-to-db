from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDockWidget, QWidget, QPushButton
from PyQt5.QtCore import Qt
from imageWidget import ImageWidget
from tableWidget import TableWidget
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("Scanned Document to Database")
        self.tableWidgets = []

        imageWidget = ImageWidget("testImages/Image.jpg", self.setTextAtFocusedField)
        self.setCentralWidget(imageWidget)

        dock = QDockWidget("Tables", self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                             Qt.DockWidgetArea.RightDockWidgetArea)
        dockWidget = QWidget(dock)
        dock.setWidget(dockWidget)
        dockLayout = QVBoxLayout(dockWidget)
        self.tableWidgets.append(TableWidget("Race", ["Year", "Series", "Class"]))
        self.tableWidgets.append(TableWidget("Results", ["Placement", "Trophy"]))
        self.tableWidgets.append(TableWidget("Sailor", ["Name", "Boat"]))
        for tw in self.tableWidgets: dockLayout.addWidget(tw)
        insertButton = QPushButton("Insert in Database")
        insertButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        insertButton.clicked.connect(self.insertInDB)
        dockLayout.addWidget(insertButton)

        self.tableWidgets[0].setFocus()
        dockWidget.setFixedSize(dockLayout.sizeHint())
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def setTextAtFocusedField(self, text):
        if self.focusWidget().text(): self.focusWidget().setText(self.focusWidget().text() + ' ' + text)
        else: self.focusWidget().setText(text)

    def insertInDB(self):
        for table in self.tableWidgets:
            print(table.objectName())
            for field in table.fields:
                print(f"\t{field.objectName()}: {field.text()}")



def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()