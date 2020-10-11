# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 00:04:12 2020

@author: Yu Zhe
"""
#Import dependencies
import sys,os
from PyQt5 import QtWidgets
import pyttsx3
import PyPDF2
import pygame                                                     # +++
pygame.init()

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

        self.pauseAudio = False
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.pause_button.clicked.connect(self.stopAudio)
        vBox.addWidget(self.pause_button)

        self.setLayout(vBox)

        quit = QtWidgets.QAction("Quit", )
        quit.triggered.connect(self.closeEvent)

    def readPage(self, page):
        self.pause_button.setText("Pause")
        self.pc.readPage(page)

    def readPages(self, start, end):
        self.pause_button.setText("Pause")
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
        if self.pauseAudio:
            self.pause_button.setText("Pause")
            self.pauseAudio = False
        else:
            self.pause_button.setText("Unpause")
            self.pauseAudio = True
        self.pc.pause_the_songs()

    def closeEvent(self, event):
        print("bye")
        pygame.mixer.music.unload()
        temp_file ='temp_voice.wav'
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
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

        self.playsound = None                                     # +++
        self.pause     = None

    def readPage(self, pg):
        temp_file ='temp_voice.wav'
        pygame.mixer.music.unload()
        if os.path.exists(temp_file):
            os.remove(temp_file)
        self.save_single_audio(pg, temp_file)
        self.data1=temp_file
        self.play_the_songs()

    def readPages(self, start, end):
        temp_file ='temp_voice.wav'
        pygame.mixer.music.unload()
        if os.path.exists(temp_file):
            os.remove(temp_file)
        self.save_audio_file(start, end, temp_file)
        self.data1=temp_file
        self.play_the_songs()

    def text2mp3(self, text, record_file='record.mp3'):
        self.speaker.save_to_file(text, record_file)
        self.speaker.runAndWait()
        self.speaker.stop() #Stops the current utterance and clears the command queue

    def save_audio_file(self, start, end, record_file='record.mp3'):
        passage=""
        for pgcount in range(start, end+1):
            pg = self.pdfBook.getPage(pgcount)
            passage += pg.extractText()
        if(record_file):
            self.text2mp3(passage, record_file)
        else:
            self.text2mp3(passage)

    def save_single_audio(self, pgcount, record_file='record.mp3'):
        pg = self.pdfBook.getPage(pgcount)
        passage = pg.extractText()
        if(record_file):
            self.text2mp3(passage, record_file)
        else:
            self.text2mp3(passage)

    def pause_the_songs(self):
        if self.playsound is None:
            self.playsound = "pause"
            pygame.mixer.music.pause()
        else:
            self.playsound = None
            pygame.mixer.music.unpause()

    def play_the_songs(self):                                     # +++
        self.playsound = pygame.mixer.init()
        pygame.mixer.music.load(self.data1)
        pygame.mixer.music.play()

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
