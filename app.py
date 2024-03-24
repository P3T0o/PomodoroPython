import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sound = None
        self.workTime = True
        self.bigBreakTime = False
        self.cycle = 0

    def initUI(self):
        self.setWindowTitle("Pomodoro by P3T0")
        self.layout = QVBoxLayout()

        self.title = QLabel("Regle ton Pomodoro")
        self.layout.addWidget(self.title)
        self.cycleLabel = QLabel("Cycle 0/4")
        self.layout.addWidget(self.cycleLabel)

        self.lineSettings = QHBoxLayout()

        self.lineWork = QVBoxLayout()
        # SpinBox pour définir le temps de travail
        self.workLabel = QLabel("Travail (minutes)")
        self.inputTimeWork = QSpinBox()
        self.inputTimeWork.setMinimum(0)  # Définit la valeur minimale à 0
        self.inputTimeWork.setMaximum(60)  # Définit la valeur maximale à 60
        self.inputTimeWork.setValue(25)
        self.inputTimeWork.setFixedSize(60, 30)  # Définit une taille fixe de 100 pixels de largeur et 30 pixels de hauteur

        self.lineBreak = QVBoxLayout()
        # SpinBox pour définir le temps de pause
        self.breakLabel = QLabel("Pause (minutes)")
        self.inputTimeBreak = QSpinBox()
        self.inputTimeBreak.setMinimum(0)  # Définit la valeur minimale à 0
        self.inputTimeBreak.setMaximum(60)  # Définit la valeur maximale à 60
        self.inputTimeBreak.setValue(5)
        self.inputTimeBreak.setFixedSize(60,30)  # Définit une taille fixe de 100 pixels de largeur et 30 pixels de hauteur

        self.lineBigBreak = QVBoxLayout()
        # SpinBox pour définir le temps de pause
        self.bigBreakLabel = QLabel("Grande Pause (minutes)")
        self.inputTimeBigBreak = QSpinBox()
        self.inputTimeBigBreak.setMinimum(0)  # Définit la valeur minimale à 0
        self.inputTimeBigBreak.setMaximum(60)  # Définit la valeur maximale à 60
        self.inputTimeBigBreak.setValue(20)
        self.inputTimeBigBreak.setFixedSize(60,30)  # Définit une taille fixe de 100 pixels de largeur et 30 pixels de hauteur

        self.lineWork.addWidget(self.workLabel)
        self.lineWork.addWidget(self.inputTimeWork)
        self.lineBreak.addWidget(self.breakLabel)
        self.lineBreak.addWidget(self.inputTimeBreak)
        self.lineBigBreak.addWidget(self.bigBreakLabel)
        self.lineBigBreak.addWidget(self.inputTimeBigBreak)

        self.lineSettings.addLayout(self.lineWork)
        self.lineSettings.addLayout(self.lineBreak)
        self.lineSettings.addLayout(self.lineBigBreak)
        self.layout.addLayout(self.lineSettings)

        self.label = QLabel("0")
        self.layout.addWidget(self.label)

        self.resetButton = QPushButton("Debuter le pomodoro")
        self.resetButton.clicked.connect(self.startTimer)
        self.layout.addWidget(self.resetButton)

        self.setFixedSize(400, 200)

        self.setLayout(self.layout)

    def initTimer(self):
        self.timer = QTimer(self)
        if self.bigBreakTime == True:
            self.timer.timeout.connect(self.updateTimerBigBreak)
        elif self.workTime == True:
            self.timer.timeout.connect(self.updateTimerWork)
        elif self.workTime == False:
            self.timer.timeout.connect(self.updateTimerBreak)
        self.timer.start(1000)
        self.seconds = 0

    def updateTimerWork(self):
        self.cycleLabel.setText(f"Cycle {self.cycle} / 4")
        self.seconds += 1
        self.label.setText(f"{self.seconds} secondes de travail")

        if self.cycle == 4:
            self.seconds = 0
            self.workTime = False
            self.bigBreakTime = True
            self.playSoundBigBreak()
            self.timer.timeout.disconnect(self.updateTimerWork)
            self.initTimer()  # Réinitialise et redémarre un nouveau cycle

        if self.seconds == self.inputTimeWork.value():  # Multiplie par 60 pour convertir les minutes en secondes
            self.playSoundBreak()
            self.showNotificationEndWork()
            self.seconds = 0
            self.workTime = False
            self.timer.timeout.disconnect(self.updateTimerWork)  # Se déconnecte de la fonction actuelle
            self.initTimer()  # Réinitialise et redémarre le minuteur avec les paramètres pour la pause

    def updateTimerBreak(self):
        self.cycleLabel.setText(f"Cycle {self.cycle} / 4")
        self.seconds += 1
        self.label.setText(f"{self.seconds} secondes de pause")

        if self.seconds == self.inputTimeBreak.value():  # Multiplie par 60 pour convertir les minutes en secondes
            self.cycle += 1
            self.playSoundWork()
            self.showNotificationEndBreak()
            self.seconds = 0
            self.workTime = True
            self.timer.timeout.disconnect(self.updateTimerBreak)  # Se déconnecte de la fonction actuelle
            self.initTimer()  # Réinitialise et redémarre le minuteur avec les paramètres pour le travail

    def updateTimerBigBreak(self):
        self.cycleLabel.setText(f"Cycle {self.cycle} / 4")
        self.seconds += 1
        self.label.setText(f"{self.seconds} secondes de grande pause")

        if self.seconds == self.inputTimeBigBreak.value():  # Multiplie par 60 pour convertir les minutes en secondes
            self.cycle = 0
            self.playSoundWork()
            self.showNotificationEndBreak()
            self.seconds = 0
            self.workTime = True
            self.bigBreakTime = False
            self.timer.timeout.disconnect(self.updateTimerBigBreak)  # Se déconnecte de la fonction actuelle
            self.initTimer()  # Réinitialise et redémarre le minuteur avec les paramètres pour le travail


    def resetTimer(self):
        self.seconds = 0
        self.label.setText("0")

    def playSoundWork(self):
        self.sound = QSound("work.wav")
        self.sound.play()

    def playSoundBreak(self):
        self.sound = QSound("break.wav")
        self.sound.play()

    def playSoundBigBreak(self):
        self.sound = QSound("bigbreak.wav")
        self.sound.play()

    def showNotificationEndWork(self):
        title = "Moment pause !"
        message = f"{self.inputTimeWork.value()} secondes se sont écoulées ! Tu mérite une pause."
        command = f'''osascript -e 'display notification "{message}" with title "{title}"' '''
        subprocess.run(command, shell=True)

    def showNotificationEndBreak(self):
        title = "On reprend !"
        message = f"{self.inputTimeBreak.value()} secondes se sont écoulées ! Retourne au travail."
        command = f'''osascript -e 'display notification "{message}" with title "{title}"' '''
        subprocess.run(command, shell=True)

    def startTimer(self):
        self.initTimer()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())
