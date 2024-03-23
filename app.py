import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound


class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.sound = None

    def initUI(self):
        self.setWindowTitle("Minuteur PyQt")
        self.layout = QVBoxLayout()

        self.label = QLabel("0")
        self.layout.addWidget(self.label)

        self.resetButton = QPushButton("Réinitialiser")
        self.resetButton.clicked.connect(self.resetTimer)
        self.layout.addWidget(self.resetButton)

        self.setFixedSize(200, 150)

        self.setLayout(self.layout)

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)
        self.seconds = 0

    def updateTimer(self):
        self.seconds += 1
        self.label.setText(f"{self.seconds} secondes")

        if self.seconds == 5:  # Vérifie si le compteur atteint 30 secondes
            self.playSound()  # Joue un son
            self.showNotification()  # Affiche une notification macOS

    def resetTimer(self):
        self.seconds = 0
        self.label.setText("0")

    def playSound(self):
        self.sound = QSound("alert.wav")
        self.sound.play()

    def showNotification(self):
        title = "Moment pause !"
        message = "30 secondes se sont écoulées !"
        command = f'''osascript -e 'display notification "{message}" with title "{title}"' '''
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())