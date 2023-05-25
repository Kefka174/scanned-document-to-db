from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QTransform
import sys

class ImageWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.setMinimumSize(800,800)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.pixmap = QPixmap(filePath)
        self.zoomDegree = 100
        self.mode = "pan" # pan, scan
        self.startSelect, self.endSelect, self.viewCenter, self.oldViewCenter = QPoint(), QPoint(), QPoint(), QPoint()

        rotateButton = QPushButton("Rotate", self)
        rotateButton.clicked.connect(self.rotateImage)
        rotateButton.setCursor(Qt.CursorShape.ArrowCursor)
        rotateButton.setGeometry(self.rect().center().x() - (rotateButton.width() // 2), 10, 75, 40)
        modeButton = QPushButton("Scan", self)
        modeButton.clicked.connect(self.setModeScan)
        modeButton.setCursor(Qt.CursorShape.ArrowCursor)
        modeButton.setGeometry(self.rect().center().x() + (modeButton.width() // 2), 10, 75, 40)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.displayPixmap = self.pixmap.scaled(self.size() * (100 / self.zoomDegree), Qt.KeepAspectRatio)
        centeredRect = self.displayPixmap.rect()
        centeredRect.moveCenter(self.rect().center() + self.viewCenter)
        painter.drawPixmap(centeredRect.topLeft(), self.displayPixmap)

        if self.startSelect != self.endSelect:
            rect = QRect(self.startSelect, self.endSelect)
            if self.mode == "scan": painter.drawRect(rect.normalized())
            elif self.mode == "pan": 
                self.viewCenter = self.oldViewCenter + QPoint(rect.width(), rect.height())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.startSelect = event.pos()
            self.endSelect = self.startSelect

            if self.mode == "pan": QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.endSelect = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            selectionRect = QRect(self.startSelect, self.endSelect).normalized()

            QApplication.restoreOverrideCursor()
            self.setModePan()
            self.oldViewCenter = self.viewCenter
            self.startSelect, self.endSelect = QPoint(), QPoint()
            self.update()

    def wheelEvent(self, event):
        degree = 1
        if event.angleDelta().y() > 0 and self.zoomDegree > 15: self.zoomDegree -= degree
        elif event.angleDelta().y() < 0 and self.zoomDegree + degree <= 100: self.zoomDegree += degree
        self.update()
    
    def rotateImage(self):
        transform = QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform)
        self.update()

    def setModeScan(self):
        self.mode = "scan"
        self.setCursor(Qt.CursorShape.CrossCursor)

    def setModePan(self):
        self.mode = "pan"
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ImageWidget("testImages/Image.jpg")
    myApp.show()

    sys.exit(app.exec_())