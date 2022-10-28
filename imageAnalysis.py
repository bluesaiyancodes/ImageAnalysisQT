import sys
import os
from tkinter.tix import Select
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QPushButton, QGridLayout, QGroupBox, QFileDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QPen

from extraCodes import *


class imgDialogue(QDialog):
    def __init__(self, h, w, imgPath, parent=None):
        super(imgDialogue, self).__init__(parent)
        self.setGeometry(500,800,w,h)
        self.setWindowTitle("Aux Image Window")
        self.imagePath = imgPath
        print("Aux Window:", self.imagePath)

        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        self.imgLabel = QLabel("Cannot Display Image", self)
        image = QImage()
        image.load(self.imagePath)
        self.pix = QPixmap.fromImage(image)
        self.imgLabel.setPixmap(self.pix)
        self.imgLabel.adjustSize()

        self.btnLab = QPushButton("LAB", self)
        self.btnRgb = QPushButton("RGB", self)

        layoutH.addWidget(self.btnLab)
        layoutH.addWidget(self.btnRgb)
        
        layoutV.addWidget(self.imgLabel)
        layoutV.addLayout(layoutH)
        
        self.setLayout(layoutV)



class mainWindow(QDialog):
    def __init__(self, imagePath, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setGeometry(500,500,900,900)
        self.setWindowTitle("Master Image Window")
        self.imagePath = imagePath
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)

        self.begin, self.destination = QPoint(), QPoint()
        self.rectList = []


        self.layout = QGridLayout(self)
        self.btnshow = QPushButton("Choose", self)
        self.btnshow.clicked.connect(self.btnShowAction)
        self.layout.addWidget(self.btnshow, 1,0, Qt.AlignRight | Qt.AlignBottom)



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        #painter.setBrush(QBrush(QColor(255, 255, 255, 255)))  -- tO fILL
        image = QImage()
        image.load(self.imagePath)
        self.pix = QPixmap.fromImage(image).scaled(900, 900, Qt.KeepAspectRatioByExpanding)
        painter.drawPixmap(self.rect(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull():
            for rect in self.rectList:
                #rect = QRect(self.begin, self.destination)
                painter.drawRect(rect.normalized())
            #rect = QRect(self.begin, self.destination)
            #painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            #print('Point 1')
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:		
            #print('Point 2')
            self.destination = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            #print('Point 3')
            rect = QRect(self.begin, self.destination)
            if rect not in self.rectList:
                self.rectList.append(rect)
            
            painter = QPainter(self.pix)
            painter.setPen(QPen(QColor(255, 255, 255, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            for rect in self.rectList:
                painter.drawRect(rect.normalized())

            #painter.drawRect(rect.normalized())
            self.begin, self.destination = QPoint(), QPoint()
        #self.update()

    def btnShowAction(self):
        print("Choose Button clicked")
        print(self.rectList[-2])
        #x, y, w, h = 
        x, y, w, h = self.rectList[-2].x(), self.rectList[-2].y(), self.rectList[-2].width(), self.rectList[-2].height()
        
        selImPath = cropImage(self.imagePath, x, y, h, w)
        print(selImPath)
        self.auxDialog = imgDialogue(imgPath=selImPath, h=h, w=w)
        
        self.auxDialog.show()



class Window(QDialog):
    def __init__(self):
        super().__init__()

        #Set Window
        self.setGeometry(500,500,200,200)
        self.setWindowTitle("Image Analysis")
      
        # Adding Label and button
        self.imgLabel = QLabel("Select an Image", self)
        self.btnChoose = QPushButton("Choose", self)
        self.btnChoose.clicked.connect(self.btnChooseAction)
        
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)
        
       # self.begin, self.destination = QPoint(), QPoint()


        self.layout = QGridLayout(self)
        #self.groupbox = QGroupBox("AR Detection", checkable=False)
        #self.layout.addWidget(self.groupbox)

        '''  
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0,0,0,0)
        self.hLayout.addWidget(self.btnChoose)
        self.hLayout.addWidget(self.btnAsses)
        '''
    
        self.layout.addWidget(self.imgLabel, 0,0, Qt.AlignCenter)
        self.layout.addWidget(self.btnChoose,1,0, Qt.AlignRight)
        #self.layout.addWidget(self.btnAsses, 2,0, Qt.AlignRight)


        #Setting Layout
        self.show()
    
    def btnChooseAction(self):
        print("Choose Button clicked")
        self.imgPath = self.open_file()
        self.imgLabel.setText(self.imgPath)
        #load image
        print("Image Path :: ", self.imgPath)
        self.dialog = mainWindow(imagePath=self.imgPath)
        
        self.dialog.show()

        


    def open_file(self):
        #path = QFileDialog.getOpenFileName(self, "Pick an Image", os.getenv('HOME'), "Images (*.png *.jpeg *.jpg *.bmp *.tif)")
        path = QFileDialog.getOpenFileName(self, "Pick an Image", os.getcwd(), "Images (*.png *.jpeg *.jpg *.bmp *.tif)")
        if path != ("", ""):
            print(path[0])
        return path[0]
    
    def load_image(self, imgPath):
        image = QImage()
        image.load(imgPath)
        self.pix = QPixmap.fromImage(image).scaled(900, 900, Qt.KeepAspectRatioByExpanding)
        # Set the pixmap using the QImage instance
        self.imgLabel.setPixmap(self.pix)
        # self.adjustSize() Auto adjusts the size of window based on the image size
        # Window Manipulation call
        self.postImgLoadWindow()
        self.update()
        
           
        
    def postImgLoadWindow(self):
        # Window Manipulation after the image is loaded
        # self.imgLabel.hide()
        return


   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window...")
