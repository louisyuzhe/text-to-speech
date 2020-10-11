# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 00:04:12 2020

@author: Yu Zhe
"""
#Import dependencies
import sys
from PyQt5 import QtWidgets
import pyttsx3
import PyPDF2

class Login(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Main Menu')

        vBox = QtWidgets.QVBoxLayout()
        
        #create pdfCoverter Obj
        self.pc = pdfCoverter('')
        self.totalPages=0;
        
        self.fileSelected = QtWidgets.QLabel("")
        self.fileSelected.setStyleSheet("border: 1px solid black;") 
        self.fileSelected.setFixedSize(300, 25)

        vBox.addWidget(self.fileSelected)
        self.button = QtWidgets.QPushButton('Load PDF')
        self.button.clicked.connect(lambda: self.get_pdf_file())
        vBox.addWidget(self.button)
        
        # Singe page
        hBox1 = QtWidgets.QHBoxLayout()

        # creating a combo box widget 
        self.combo_box1 = QtWidgets.QComboBox(self)       
        # adding list of items to combo box 
        hBox1.addWidget(self.combo_box1)

        # Read
        self.button = QtWidgets.QPushButton('Read single page')
        self.button.clicked.connect(lambda: self.readPage(int(self.combo_box1.currentText())))
        hBox1.addWidget(self.button)
        
        # Save as mp3
        self.button = QtWidgets.QPushButton('Save as mp3')
        self.button.clicked.connect(lambda: self.pageToMp3(int(self.combo_box1.currentText())))
        hBox1.addWidget(self.button)
        
        vBox.addLayout(hBox1)
        
        # Multi pages
        hBox2 = QtWidgets.QHBoxLayout()
        
        # creating a combo box widget 
        self.combo_box2 = QtWidgets.QComboBox(self) 
        self.combo_box3 = QtWidgets.QComboBox(self)       
        # adding list of items to combo box 
        hBox2.addWidget(self.combo_box2)
        hBox2.addWidget(self.combo_box3)

        self.button = QtWidgets.QPushButton('Read multiple pages')
        self.button.clicked.connect(lambda: self.readPages(int(self.combo_box2.currentText()), int(self.combo_box3.currentText())))
        hBox2.addWidget(self.button)
        
        # Save as mp3
        self.button = QtWidgets.QPushButton('Save as mp3')
        self.button.clicked.connect(lambda: self.multiPageToMp3(int(self.combo_box2.currentText()), int(self.combo_box3.currentText())))
        hBox2.addWidget(self.button)
        
        vBox.addLayout(hBox2)

        self.button = QtWidgets.QPushButton('Stop audio')
        self.button.clicked.connect(lambda: self.stopAudio())
        vBox.addWidget(self.button)
        
        self.setLayout(vBox)

    def readPage(self, page):
        self.pc.stopSpeaking = False
        self.pc.readPage(page)
    
    def readPages(self, start, end):
        self.pc.stopSpeaking = False
        self.pc.readPages(start, end)
    
    def pageToMp3(self, page):
        self.pc.save_single_audio(page)
     
    def multiPageToMp3(self, start, end):
        self.pc.save_audio_file(start, end)
        
    def get_pdf_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open PDF File', r"", "PDF files (*.pdf)")
        self.fileSelected.setText(file_name)
        self.pc = pdfCoverter(file_name)
        self.totalPages = self.pc.totalPg
        page = list([str(x) for x in range(1, self.totalPages)])
        self.combo_box1.addItems(page) 
        self.combo_box2.addItems(page) 
        self.combo_box3.addItems(page) 

    def stopAudio(self):
        self.pc.stopSpeaking = True
        
        
class pdfCoverter:
    
    def __init__(self, filepath):
        self.speaker = pyttsx3.init()
        """ Voice Setting """
        self.speaker.setProperty('rate', 135) # set new speaking rate
        voices = self.speaker.getProperty('voices') # Get details of current voice
        self.speaker.setProperty('voice', voices[1].id) # Set female voice
        
        if(filepath != ''):
            pdf = open(filepath, 'rb')
            self.pdfBook = PyPDF2.PdfFileReader(pdf)
            self.totalPg = self.pdfBook.numPages
        
        self.stopSpeaking = False
        
    def readPage(self, pg):
        page = self.pdfBook.getPage(pg)
        passage = page.extractText()
        arr = passage.splitlines()
        for sentence in arr:
            if (self.stopSpeaking == True):
                break
            self.speaker.say(sentence)
            self.speaker.runAndWait()
        self.speaker.stop() #Stops the current utterance and clears the command queue
        
    def readPages(self, start, end):
        for pgcount in range(start, end+1):
            pg = self.pdfBook.getPage(pgcount)
            passage = pg.extractText()
            arr = passage.splitlines()
            for sentence in arr:
                if (self.stopSpeaking == True):
                    break
                self.speaker.say(sentence)
                self.speaker.runAndWait()
        self.speaker.stop() #Stops the current utterance and clears the command queue
    
    def text2mp3(self, text):
        self.speaker.save_to_file(text, 'record.mp3')
        self.speaker.runAndWait()
        self.speaker.stop() #Stops the current utterance and clears the command queue
    
    def save_audio_file(self, start, end):
        passage=""
        for pgcount in range(start, end+1):
            pg = self.pdfBook.getPage(pgcount)
            passage += pg.extractText()
        self.text2mp3(passage)   
    
    def save_single_audio(self, pgcount):
        pg = self.pdfBook.getPage(pgcount)
        passage = pg.extractText()
        self.text2mp3(passage)   
    
class Controller:

    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.show()

 
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()