import sys
import os
from tkinter.tix import Select
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QPushButton, QGridLayout, QGroupBox, QFileDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QImage, QPixmap, QBrush, QColor, QPen

from extraCodes import *


class imgDialogue(QDialog):
    '''
    This Class creates new windows for the selected boxes in the main image screen
    '''

    def __init__(self, h, w, imgPath, parent=None):
        super(imgDialogue, self).__init__(parent)
        self.setGeometry(500,800,w,h)
        self.setWindowTitle("Aux Image Window")
        self.imagePath = imgPath
        #print("Aux Window:", self.imagePath)

        # Set Layouts
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()

        # Set Image
        self.imgLabel = QLabel("Cannot Display Image", self)
        image = QImage()
        image.load(self.imagePath)
        self.pix = QPixmap.fromImage(image)
        self.imgLabel.setPixmap(self.pix)
        self.imgLabel.adjustSize()

        # Declare Buttons
        self.btnLab = QPushButton("LAB", self)
        self.btnRgb = QPushButton("RGB", self)

        # Configure Layout
        layoutH.addWidget(self.btnLab)
        layoutH.addWidget(self.btnRgb)
        
        layoutV.addWidget(self.imgLabel)
        layoutV.addLayout(layoutH)
        
        self.setLayout(layoutV)



class mainWindow(QDialog):
    '''
        This window displays the image on where the boxes will be drawn
    '''
    def __init__(self, imagePath, parent=None):
        super(mainWindow, self).__init__(parent)
        # Set Window Configuration
        self.setGeometry(500,500,900,900)
        self.setWindowTitle("Master Image Window")
        self.imagePath = imagePath
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)

        # Pointers for rectangle box drawing
        self.begin, self.destination = QPoint(), QPoint()
        # To keep a list of of all the boxes
        self.rectList = []


        # Resize image based on the window size
        self.imagePath = resize_with_padding(self.imagePath, (900, 900))

        # Adding a button and setting its action 
        self.layout = QGridLayout(self)
        self.btnshow = QPushButton("Show", self)
        self.btnshow.clicked.connect(self.btnShowAction)
        self.layout.addWidget(self.btnshow, 1,0, Qt.AlignRight | Qt.AlignBottom)

        # for multiple window management - counts the number of windows initialized
        self.winArr = 0



    def paintEvent(self, event):
        # Initialize Painter
        painter = QPainter(self)
        # Set Pen color for box line color
        painter.setPen(QPen(QColor(255, 255, 255, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        #painter.setBrush(QBrush(QColor(255, 255, 255, 255)))  -- tO fILL
        
        # initialize image
        image = QImage()
        # Load image
        image.load(self.imagePath)
        # self.pix = QPixmap.fromImage(image).scaled(900, 900, Qt.KeepAspectRatioByExpanding)
        self.pix = QPixmap.fromImage(image)
        # Set Image as window image
        painter.drawPixmap(self.rect(), self.pix)

        # Begin Drawing of drawn Box
        if not self.begin.isNull() and not self.destination.isNull():
            # Draw all the boxes present in the box list
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
            # append to the the box list of not present
            if rect not in self.rectList:

                self.rectList.append(rect)
            
            # Draw all the boxes present in the box list
            painter = QPainter(self.pix)
            painter.setPen(QPen(QColor(255, 255, 255, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            for rect in self.rectList:
                painter.drawRect(rect.normalized())

            # reset the coordinated used for drawing the boxes
            self.begin, self.destination = QPoint(), QPoint()
        #self.update()

    def cleanRectList(self):
        for i in range(len(self.rectList)):
            if self.rectList[i].width()==1:
                self.rectList.remove(self.rectList[i])
                i-=1
                


    def btnShowAction(self):
        print("Show Button clicked")
        self.cleanRectList()
        print(self.rectList[-1])
        #x, y, w, h = 
        x, y, w, h = self.rectList[-1].x(), self.rectList[-1].y(), self.rectList[-1].width(), self.rectList[-1].height()
        
        selImPath = cropImage(self.imagePath, x, y, h, w)
        print(selImPath)

        # Creating Multiple Aux Windows (Upto 5)
        
        self.auxWins = {}
        self.auxWins[self.winArr + 1] = imgDialogue(imgPath=selImPath, h=h, w=w)
        self.auxWins[self.winArr + 1].show()
        self.winArr += 1
        print(self.auxWins)

        for i in self.auxWins.values():
            print(i)



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
