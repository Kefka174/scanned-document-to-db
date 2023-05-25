from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QTransform
import sys

class ImageWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.pixmap = QPixmap(filePath)
        self.zoomDegree = 100
        self.mode = "view" # view, select
        self.startSelect, self.endSelect, self.viewCenter, self.oldViewCenter = QPoint(), QPoint(), QPoint(), QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.displayPixmap = self.pixmap.scaled(self.size() * (100 / self.zoomDegree), Qt.KeepAspectRatio)
        centeredRect = self.displayPixmap.rect()
        centeredRect.moveCenter(self.rect().center() + self.viewCenter)
        painter.drawPixmap(centeredRect.topLeft(), self.displayPixmap)

        if self.startSelect != self.endSelect:
            rect = QRect(self.startSelect, self.endSelect)
            if self.mode == "select": painter.drawRect(rect.normalized())
            elif self.mode == "view": 
                self.viewCenter = self.oldViewCenter + QPoint(rect.width(), rect.height())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.startSelect = event.pos()
            self.endSelect = self.startSelect

            if self.mode == "view": QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.endSelect = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            selectionRect = QRect(self.startSelect, self.endSelect).normalized()

            QApplication.restoreOverrideCursor()
            self.mode = "view"
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.oldViewCenter = self.viewCenter
            self.startSelect, self.endSelect = QPoint(), QPoint()
            self.update()

    def wheelEvent(self, event):
        degree = 1
        if event.angleDelta().y() > 0 and self.zoomDegree > 15: self.zoomDegree -= degree
        elif event.angleDelta().y() < 0 and self.zoomDegree + degree <= 100: self.zoomDegree += degree
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R: self.rotateImage()
        elif event.key() == Qt.Key_V: 
            self.mode = "view"
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        elif event.key() == Qt.Key_S: 
            self.mode = "select"
            self.setCursor(Qt.CursorShape.CrossCursor)
    
    def rotateImage(self):
        transform = QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform)
        self.update()

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ImageWidget("testImages/Image.jpg")
    myApp.show()

    sys.exit(app.exec_())