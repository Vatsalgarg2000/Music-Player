import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt,QTimer
import random,time
from pygame import mixer
from mutagen.mp3 import MP3 #helps in calculating length of the song
import Style


musicList=[]
mixer.init() #globally initiaizing a mixer
muted=False
count=0
songLength=0
index=0


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(450,150,480,700)

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.progressBar=QProgressBar()
        self.progressBar.setTextVisible(False) #removes the percent text after progress bar
        self.progressBar.setStyleSheet(Style.progressBarStyle())

        self.songTimerLabel=QLabel("0:00")
        self.songLengthLabel=QLabel("/ 0:00")

        #if we want to use images for our buttons, we need to use tool buttons
        self.addButton = QToolButton()
        self.addButton.setIcon(QIcon("icons/add.png"))
        self.addButton.setIconSize(QSize(48,48))
        self.addButton.setToolTip("Add a Song") # When we move cursor above the button, a hints appears on what the button does
        self.addButton.clicked.connect(self.addSound)

        self.shuffleButton = QToolButton()
        self.shuffleButton.setIcon(QIcon("icons/shuffle.png"))
        self.shuffleButton.setIconSize(QSize(48, 48))
        self.shuffleButton.setToolTip("Shuffle Playlist")
        self.shuffleButton.clicked.connect(self.shufflePlayList)

        self.previousButton = QToolButton()
        self.previousButton.setIcon(QIcon("icons/previous.png"))
        self.previousButton.setIconSize(QSize(48, 48))
        self.previousButton.setToolTip("Play Previous")
        self.previousButton.clicked.connect(self.playPrevious)

        self.playButton = QToolButton()
        self.playButton.setIcon(QIcon("icons/play.png"))
        self.playButton.setIconSize(QSize(64, 64))
        self.playButton.setToolTip("Play")
        self.playButton.clicked.connect(self.playSounds)

        self.nextButton = QToolButton()
        self.nextButton.setIcon(QIcon("icons/next.png"))
        self.nextButton.setIconSize(QSize(48, 48))
        self.nextButton.setToolTip("Play Next")
        self.nextButton.clicked.connect(self.playNext)

        self.muteButton = QToolButton()
        self.muteButton.setIcon(QIcon("icons/mute.png"))
        self.muteButton.setIconSize(QSize(24, 24))
        self.muteButton.setToolTip("Mute")
        self.muteButton.clicked.connect(self.muteSound)

        self.volumeSlider=QSlider(Qt.Horizontal)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.setValue(70)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setMinimum(0)
        mixer.music.set_volume(0.7) # as range for mixer is in between 0-1
        self.volumeSlider.valueChanged.connect(self.setVolume)

        self.playList=QListWidget()
        self.playList.doubleClicked.connect(self.playSounds) # Plays music with double click also
        self.playList.setStyleSheet(Style.playListStyle())

        self.timer=QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgressBar)

        self.songName=QLabel("                                                   ")
        self.songName.setStyleSheet("font:12pt Times Bold;color:white")


    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topMainLayout=QVBoxLayout()
        self.topGroupBox=QGroupBox("Music Player")
        self.topGroupBox.setStyleSheet(Style.groupboxStyle())
        #for layouts,we cannot use style sheet but we can use groupBox for changing colors of background. Also group box has title which is good for us
        self.topLayout=QHBoxLayout()
        self.middleLayout=QHBoxLayout()
        self.bottomLayout=QVBoxLayout()

        self.topLayout.addWidget(self.progressBar)
        self.topLayout.addWidget(self.songTimerLabel)
        self.topLayout.addWidget(self.songLengthLabel)

        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.addButton)
        self.middleLayout.addWidget(self.shuffleButton)
        self.middleLayout.addWidget(self.previousButton)
        self.middleLayout.addWidget(self.playButton)
        self.middleLayout.addWidget(self.nextButton)
        self.middleLayout.addWidget(self.volumeSlider)
        self.middleLayout.addWidget(self.muteButton)
        self.middleLayout.addStretch()

        self.bottomLayout.addWidget(self.playList)

        self.topMainLayout.addStretch()
        self.topMainLayout.addWidget(self.songName)
        self.topMainLayout.addLayout(self.topLayout)
        self.topMainLayout.addLayout(self.middleLayout)
        self.topGroupBox.setLayout(self.topMainLayout)
        #if we wanted to change background of only progress bar and not buttons, we could have use self.topGroupBox.setLayout(self.topLayout)
        self.mainLayout.addWidget(self.topGroupBox,25)
        self.mainLayout.addLayout(self.bottomLayout,75)

        self.setLayout(self.mainLayout)

    def addSound(self):
        #we are going to use PlayGame for sounds which supports the following extensions
        directory=QFileDialog.getOpenFileName(self,"Add Sound","","Sound Files (*.mp3 *.ogg *.wav)") #gives full path of the song
        filename=os.path.basename(directory[0]) #gives only last part of the song
        self.playList.addItem(filename)
        musicList.append(directory[0])

    def shufflePlayList(self):
        random.shuffle(musicList)
        self.playList.clear()
        for song in musicList:
            filename = os.path.basename(song)
            self.playList.addItem(filename)

    def playSounds(self):
        global songLength
        global count
        global index
        count=0
        if self.playList.selectedItems():
            index=self.playList.currentRow()
            try:
                mixer.music.load(str(musicList[index]))
                mixer.music.play()
                self.timer.start()
                sound = MP3(str(musicList[index]))

                filename = os.path.basename(musicList[index])
                self.songName.setText(filename)

                songLength=sound.info.length #gives the length of song in seconds -> eg=123.456644333, so to remove decimal places, we use round function
                songLength=round(songLength)
                min, sec = divmod(songLength, 60)
                if sec >= 10:
                    self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
                else:
                    self.songLengthLabel.setText("/ " + str(min) + ":0" + str(sec))

                #self.progressBar.setValue(0)
                self.progressBar.setMaximum(songLength)

            except:
                pass

        else:
            QMessageBox.information(self, "Warning!!!", "Song has not been selected")

    def playPrevious(self):
        global songLength
        global count
        global index
        count = 0
        items=self.playList.count()
        if index==0:
            index=items

        index-=1
        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))

            filename = os.path.basename(musicList[index])
            self.songName.setText(filename)

            songLength = sound.info.length  # gives the length of song in seconds -> eg=123.456644333, so to remove decimal places, we use round function
            songLength = round(songLength)
            min, sec = divmod(songLength, 60)
            if sec >= 10:
                self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            else:
                self.songLengthLabel.setText("/ " + str(min) + ":0" + str(sec))

            # self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def playNext(self):
        global songLength
        global count
        global index
        count = 0
        items=self.playList.count()
        index+=1
        if index==items:
            index=0

        try:
            mixer.music.load(str(musicList[index]))
            mixer.music.play()
            self.timer.start()
            sound = MP3(str(musicList[index]))

            filename = os.path.basename(musicList[index])
            self.songName.setText(filename)

            songLength = sound.info.length  # gives the length of song in seconds -> eg=123.456644333, so to remove decimal places, we use round function
            songLength = round(songLength)
            min, sec = divmod(songLength, 60)
            if sec >= 10:
                self.songLengthLabel.setText("/ " + str(min) + ":" + str(sec))
            else:
                self.songLengthLabel.setText("/ " + str(min) + ":0" + str(sec))

            # self.progressBar.setValue(0)
            self.progressBar.setMaximum(songLength)

        except:
            pass

    def setVolume(self):
        self.volume=self.volumeSlider.value()
        mixer.music.set_volume(self.volume/100) #as mixer has range of 0-1

    def muteSound(self):
        global muted
        if muted==False:
            mixer.music.set_volume(0.0)
            muted=True
            self.muteButton.setIcon(QIcon("icons/unmuted.png"))
            self.muteButton.setToolTip("Unmute")
            self.volumeSlider.setValue(0)

        else:
            mixer.music.set_volume(0.7)
            muted=False
            self.muteButton.setIcon(QIcon("icons/mute.png"))
            self.muteButton.setToolTip("Mute")
            self.volumeSlider.setValue(70)

    def updateProgressBar(self):
        global count
        global songLength
        count+=1
        self.progressBar.setValue(count)
        self.songTimerLabel.setText(time.strftime("%M:%S",time.gmtime(count)))
        if count==songLength:
            self.timer.stop()



def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
