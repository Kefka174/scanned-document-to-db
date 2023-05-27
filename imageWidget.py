from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QTransform
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
        self.startSelect, self.endSelect, self.viewCenter, self.oldViewCenter = QPoint(), QPoint(), QPoint(), QPoint()

        rotateButton = QPushButton("Rotate", self)
        rotateButton.clicked.connect(self.rotateImage)
        rotateButton.setCursor(Qt.CursorShape.ArrowCursor)
        rotateButton.setGeometry(self.rect().center().x() - (rotateButton.width() // 2), 10, 75, 40)
        modeButton = QPushButton("Scan", self)
        modeButton.clicked.connect(self.setModeScan)
        modeButton.setCursor(Qt.CursorShape.ArrowCursor)
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
        centeredRect.moveCenter(self.rect().center() + self.viewCenter)
        painter.drawPixmap(centeredRect.topLeft(), self.displayPixmap)

        if self.startSelect != self.endSelect:
            rect = QRect(self.startSelect, self.endSelect)
            if self.mode == "scan": painter.drawRect(rect.normalized())
            elif self.mode == "panview": 
                self.viewCenter = self.oldViewCenter + QPoint(rect.width(), rect.height())
        if self.contours:
            for rect, text in self.contours:
                painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.startSelect = event.pos()
            self.endSelect = self.startSelect

            if self.mode == "panview": QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
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

            QApplication.restoreOverrideCursor()
            self.setModePanView()
            self.oldViewCenter = self.viewCenter
            self.startSelect, self.endSelect = QPoint(), QPoint()
            self.update()

    def wheelEvent(self, event):
        degree = 1
        if event.angleDelta().y() > 0 and self.zoomDegree > 15: self.zoomDegree -= degree
        elif event.angleDelta().y() < 0 and self.zoomDegree + degree <= 100: self.zoomDegree += degree
        self.update()
    
    def rotateImage(self):
        self.cvOriginal = cv2.rotate(self.cvOriginal, cv2.ROTATE_90_CLOCKWISE)
        self.cvDilated = cv2.rotate(self.cvDilated, cv2.ROTATE_90_CLOCKWISE)
        transform = QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform)
        self.update()

    def setModeScan(self):
        self.mode = "scan"
        self.setCursor(Qt.CursorShape.CrossCursor)

    def setModePanView(self):
        self.mode = "panview"
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def displayRectToImageRect(self, displayRect):
        imageRect = displayRect

        # descale
        imageRect.setHeight(int(imageRect.height() * self.pixmap.height() / self.displayPixmap.height()))
        imageRect.setWidth(int(imageRect.width() * self.pixmap.width() / self.displayPixmap.width()))

        # de-center
        displayRectDistanceToCenterHeight = displayRect.top() - (self.rect().center().y() + self.viewCenter.y())
        imageRectDistanceToCenterHeight = displayRectDistanceToCenterHeight * self.pixmap.height() / self.displayPixmap.height()
        imageRect.moveTop(int(self.pixmap.rect().center().y() + imageRectDistanceToCenterHeight))

        displayRectDistanceToCenterWidth = displayRect.left() - (self.rect().center().x() + self.viewCenter.x())
        imageRectDistanceToCenterWidth = displayRectDistanceToCenterWidth * self.pixmap.width() / self.displayPixmap.width()
        imageRect.moveLeft(int(self.pixmap.rect().center().x() + imageRectDistanceToCenterWidth))

        # cut off out-of-bounds part of rect
        if imageRect.left() < 0: imageRect.setLeft(0)
        if imageRect.right() > self.pixmap.width(): imageRect.setRight(self.pixmap.width())
        if imageRect.top() < 0: imageRect.setTop(0)
        if imageRect.bottom() > self.pixmap.height(): imageRect.setBottom(self.pixmap.height())

        return imageRect


    def scan(self, displayRect):
        imageRect = self.displayRectToImageRect(displayRect)
        scanDilatedImage = self.cvDilated[imageRect.y():imageRect.y() + imageRect.height(), imageRect.x():imageRect.x() + imageRect.width()]
        scanImage = self.cvOriginal[imageRect.y():imageRect.y() + imageRect.height(), imageRect.x():imageRect.x() + imageRect.width()]
        contours, hierarchy = cv2.findContours(scanDilatedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # convert contour to text
            contourImage = cv2.copyMakeBorder(scanImage[y:y + h, x:x + w], h, h, w, w, cv2.BORDER_REPLICATE)
            text = pytesseract.image_to_string(contourImage)

            if text: 
                print(text)
                rect = QRect(x, y, w, h)
                # move center
                # scale
                # self.contours.append((rect, text))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    myApp = ImageWidget("testImages/Image.jpg")
    myApp.show()

    sys.exit(app.exec_())