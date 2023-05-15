from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QTransform
import sys

class ImageWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.setMinimumSize(1200, 800)
        self.setLayout(QVBoxLayout())

        self.pixmap = QPixmap(filePath)
        self.zoomDegree = 100
        self.startDrag, self.endDrag = QPoint(), QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.displayPixmap = self.pixmap.scaled(self.size() * (100 / self.zoomDegree), Qt.KeepAspectRatio)
        centeredRect = self.displayPixmap.rect()
        centeredRect.moveCenter(self.rect().center())
        painter.drawPixmap(centeredRect.topLeft(), self.displayPixmap)

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
            selectionRect = QRect(self.startDrag, self.endDrag).normalized()

            self.startDrag, self.endDrag = QPoint(), QPoint()
            self.update()

    def wheelEvent(self, event):
        degree = 1
        if event.angleDelta().y() > 0 and self.zoomDegree > 15: self.zoomDegree -= degree
        elif event.angleDelta().y() < 0 and self.zoomDegree + degree <= 100: self.zoomDegree += degree
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R: self.rotateImage()
    
    def rotateImage(self):
        transform = QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform)
        self.update()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ImageWidget("testImages/Image.jpg")
    myApp.show()

    sys.exit(app.exec_())