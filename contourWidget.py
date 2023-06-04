from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QRect
import sys

class ContourWidget(QLabel):
    def __init__(self, parent, geometryRect, text, clickFunction):
        super().__init__(parent)
        self.text = text
        self.clickFunction = clickFunction
        self.setGeometry(geometryRect)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clickFunction(self.text)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ContourWidget(None, QRect(300, 300, 100, 100), "Test")
    myApp.show()

    sys.exit(app.exec_())