#Installation requirements: python, pyqt5, OpenCV-Python.  

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QLabel
import sys
import os
import cv2
import shutil
import subprocess

def detectFaces(path):
    '''
    Indicates if there are human faces in an image by returning a boolean value.
    '''
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Reads the image.
    img = cv2.imread(path)

    # Converts image into grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detects faces.
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        return True
    else:
        return False

class Window(QMainWindow):

    filename = 'No files' 

    def __init__(self):
        super().__init__()

        self.title = "FaceDetect"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 350

        self.InitWindow()

    def InitWindow(self):
        '''
        Initial components displayed in the application window.
        '''

        label_str = """Instructions: Select 1 or multiple images using 'choose images' and press 'filter images'. This will create a 
                     new folder containing the images selected which contain at least 1 person.""" 

        self.label = QLabel(label_str, self)
        self.label.setGeometry(100,0,650,200)

        self.choosebutton = QPushButton("Choose images", self)
        self.choosebutton.setGeometry(100,140,100,50)
        self.choosebutton.clicked.connect(self.openFileDialog)

        self.createbutton = QPushButton("Filter images", self)
        self.createbutton.setGeometry(100,195,100,50)
        self.createbutton.clicked.connect(self.createFolder)

        self.textedit = QTextEdit(self)
        self.textedit.setGeometry(200,141,400,103)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.show()

    def openFileDialog(self):
        '''
        Function which allows user to select files in windows explorer. 
        '''
        global filename

        filename = QFileDialog.getOpenFileNames(self, 'Open Files')

        if filename[0]:
            self.textedit.setText(str(filename[0]))

    def createFolder(self):
        '''
        Identifies which images provided contain people, and creates a new folder containing
        copies of these images. 
        '''
        global filename

        filecount = 1
        
        #Creates a new folder with name not used by any existing folders.
        while filecount >= 1:
            try:
               os.mkdir('Images containing people ' + str(filecount))
            except:
                filecount +=1
            else:
                dst_folder = 'Images containing people ' + str(filecount)
                filecount = 0

        #Copies images with people to the new folder.
        for image in filename[0]:
            if detectFaces(image) == True:
               shutil.copy(image, dst_folder)

        #Takes the user to the new folder in windows explorer.
        subprocess.Popen('explorer "'+dst_folder+'"')

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())

