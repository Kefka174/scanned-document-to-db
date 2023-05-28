from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QTransform, QPen, QColor
import pytesseract
import cv2
import sys

class ImageWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.filePath = filePath
        self.guiInit()
        self.cvInit()

    def guiInit(self):
        self.setMinimumSize(800,800)
        self.setModePanView()
        self.pixmap = QPixmap(self.filePath)
        self.zoomDegree = 100
        self.contours = []
        self.startSelect, self.endSelect, self.viewTopLeft, self.oldViewTopLeft = QPoint(), QPoint(), QPoint(), QPoint()

        rotateButton = QPushButton("Rotate", self)
        rotateButton.clicked.connect(self.rotateImage)
        rotateButton.setGeometry(self.rect().center().x() - (rotateButton.width() // 2), 10, 75, 40)
        modeButton = QPushButton("Scan", self)
        modeButton.clicked.connect(self.setModeScan)
        modeButton.setGeometry(self.rect().center().x() + (modeButton.width() // 2), 10, 75, 40)

    def cvInit(self):
        self.cvOriginal = cv2.imread(self.filePath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_IGNORE_ORIENTATION)
        ret, thresh1 = cv2.threshold(self.cvOriginal, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
        self.cvDilated = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.displayPixmap = self.pixmap.scaled(self.size() * (100 / self.zoomDegree), Qt.KeepAspectRatio)
        centeredRect = self.displayPixmap.rect()
        centeredRect.moveCenter(self.rect().center() + self.viewTopLeft)
        painter.drawPixmap(centeredRect.topLeft(), self.displayPixmap)

        if self.startSelect != self.endSelect:
            if self.mode == "scan": painter.drawRect(QRect(self.startSelect, self.endSelect).normalized())
            elif self.mode == "panview": 
                self.viewTopLeft = self.oldViewTopLeft + QPoint(self.endSelect - self.startSelect)
        if self.contours:
            for contourRect, text in self.contours:
                painter.setPen(QPen(QColor("lightgreen"), 3))
                painter.drawRect(contourRect)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.startSelect = event.pos()
            self.endSelect = self.startSelect

            if self.mode == "panview": QApplication.setOverrideCursor(Qt.CursorShape.SizeAllCursor)
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.endSelect = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.mode == "scan":
                displayRect = QRect(self.startSelect, self.endSelect).normalized()
                self.scan(displayRect)
            if self.mode == "panview":
                QApplication.restoreOverrideCursor()
                self.oldViewTopLeft = self.viewTopLeft

            self.startSelect, self.endSelect = QPoint(), QPoint()
            self.setModePanView()
            self.update()

    def wheelEvent(self, event):
        oldZoomDegree = self.zoomDegree
        # Scale
        degreeChange = 1
        if event.angleDelta().y() > 0 and self.zoomDegree > 15: self.zoomDegree -= degreeChange
        elif event.angleDelta().y() < 0 and self.zoomDegree + degreeChange <= 100: self.zoomDegree += degreeChange
        # Center on cursor
        self.viewTopLeft += (self.rect().center() + self.viewTopLeft - event.pos()) * (oldZoomDegree / self.zoomDegree - 1)
        self.oldViewTopLeft = self.viewTopLeft

        self.update()
    
    def rotateImage(self):
        self.cvOriginal = cv2.rotate(self.cvOriginal, cv2.ROTATE_90_CLOCKWISE)
        self.cvDilated = cv2.rotate(self.cvDilated, cv2.ROTATE_90_CLOCKWISE)
        transform = QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform)
        self.update()

    def setModeScan(self):
        self.contours.clear()
        self.mode = "scan"
        self.setCursor(Qt.CursorShape.CrossCursor)

    def setModePanView(self):
        self.mode = "panview"
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def displayRectToImageRect(self, displayRect):
        imageRect = QRect(displayRect)
        # Descale
        imageRect.setHeight(int(imageRect.height() * self.pixmap.height() / self.displayPixmap.height()))
        imageRect.setWidth(int(imageRect.width() * self.pixmap.width() / self.displayPixmap.width()))
        # De-center
        displayRectDistanceToCenterHeight = displayRect.top() - (self.rect().center().y() + self.viewTopLeft.y())
        imageRectDistanceToCenterHeight = displayRectDistanceToCenterHeight * self.pixmap.height() / self.displayPixmap.height()
        imageRect.moveTop(int(self.pixmap.rect().center().y() + imageRectDistanceToCenterHeight))

        displayRectDistanceToCenterWidth = displayRect.left() - (self.rect().center().x() + self.viewTopLeft.x())
        imageRectDistanceToCenterWidth = displayRectDistanceToCenterWidth * self.pixmap.width() / self.displayPixmap.width()
        imageRect.moveLeft(int(self.pixmap.rect().center().x() + imageRectDistanceToCenterWidth))
        # Cut off out-of-bounds part of rect
        if imageRect.left() < 0: imageRect.setLeft(0)
        if imageRect.top() < 0: imageRect.setTop(0)
        if imageRect.bottom() > self.pixmap.height(): imageRect.setBottom(self.pixmap.height())
        if imageRect.right() > self.pixmap.width(): imageRect.setRight(self.pixmap.width())
        return imageRect
    
    def imageRectToDisplayRect(self, imageRect):
        displayRect = QRect(imageRect)
        # Scale
        displayRect.setHeight(int(displayRect.height() * self.displayPixmap.height() / self.pixmap.height()))
        displayRect.setWidth(int(displayRect.width() * self.displayPixmap.width() / self.pixmap.width()))
        # Re-center
        imageRectDistanceToCenterHeight = imageRect.top() - self.pixmap.rect().center().y()
        displayRectDistanceToCenterHeight = imageRectDistanceToCenterHeight * self.displayPixmap.height() / self.pixmap.height()
        displayRect.moveTop(int(self.rect().center().y() + self.viewTopLeft.y() + displayRectDistanceToCenterHeight))

        imageRectDistanceToCenterWidth = imageRect.left() - self.pixmap.rect().center().x()
        displayRectDistanceToCenterWidth = imageRectDistanceToCenterWidth * self.displayPixmap.width() / self.pixmap.width()
        displayRect.moveLeft(int(self.rect().center().x() + self.viewTopLeft.x() + displayRectDistanceToCenterWidth))
        return displayRect

    def scan(self, displayRect):
        imageRect = self.displayRectToImageRect(displayRect)
        scanDilatedImage = self.cvDilated[imageRect.y():imageRect.y() + imageRect.height(), imageRect.x():imageRect.x() + imageRect.width()]
        scanImage = self.cvOriginal[imageRect.y():imageRect.y() + imageRect.height(), imageRect.x():imageRect.x() + imageRect.width()]
        contours, hierarchy = cv2.findContours(scanDilatedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Convert contour to text
            contourImage = cv2.copyMakeBorder(scanImage[y:y + h, x:x + w], h, h, w, w, cv2.BORDER_REPLICATE)
            text = pytesseract.image_to_string(contourImage)

            if text: 
                rect = self.imageRectToDisplayRect(QRect(x + imageRect.x(), y + imageRect.y(), w, h))
                self.contours.append((rect, text))
        QApplication.restoreOverrideCursor()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ImageWidget("testImages/Image.jpg")
    myApp.show()

    sys.exit(app.exec_())