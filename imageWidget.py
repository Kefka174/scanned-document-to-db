from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter
import sys

class ImageWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.setMinimumSize(1200, 800)
        self.setLayout(QVBoxLayout())

        self.pixmap = QPixmap(filePath)
        self.startDrag, self.endDrag = QPoint(), QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        scaledPixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        scaledRect = scaledPixmap.rect()
        scaledRect.moveCenter(self.rect().center())
        painter.drawPixmap(scaledRect.topLeft(), scaledPixmap)

        if not self.startDrag.isNull() and not self.endDrag.isNull():
            rect = QRect(self.startDrag, self.endDrag)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.startDrag = event.pos()
            self.endDrag = self.startDrag
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:	
            self.endDrag = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            self.startDrag, self.endDrag = QPoint(), QPoint()
            self.update()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ImageWidget("testImages/Image.jpg")
    myApp.show()

    sys.exit(app.exec_())