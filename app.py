import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.sound = None

    def initUI(self):
        self.setWindowTitle("Pomodoro by P3T0")
        self.layout = QVBoxLayout()

        self.title = QLabel("Regle ton Pomodoro")
        self.layout.addWidget(self.title)

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

        self.lineWork.addWidget(self.workLabel)
        self.lineWork.addWidget(self.inputTimeWork)
        self.lineBreak.addWidget(self.breakLabel)
        self.lineBreak.addWidget(self.inputTimeBreak)

        self.lineSettings.addLayout(self.lineWork)
        self.lineSettings.addLayout(self.lineBreak)
        self.layout.addLayout(self.lineSettings)

        self.label = QLabel("0")
        self.layout.addWidget(self.label)

        self.resetButton = QPushButton("Réinitialiser")
        self.resetButton.clicked.connect(self.resetTimer)
        self.layout.addWidget(self.resetButton)

        self.setFixedSize(400, 200)

        self.setLayout(self.layout)

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)
        self.seconds = 0

    def updateTimer(self):
        self.seconds += 1
        self.label.setText(f"{self.seconds} secondes")

        # Utilise la valeur du QSpinBox comme condition
        if self.seconds == self.inputTimeWork.value():
            self.playSound()  # Joue un son
            self.showNotification()  # Affiche une notification macOS
            self.resetTimer()  # Réinitialise le minuteur automatiquement

    def resetTimer(self):
        self.seconds = 0
        self.label.setText("0")

    def playSound(self):
        self.sound = QSound("alert.wav")
        self.sound.play()

    def showNotification(self):
        title = "Moment pause !"
        message = f"{self.inputTimeWork.value()} secondes se sont écoulées !"
        command = f'''osascript -e 'display notification "{message}" with title "{title}"' '''
        subprocess.run(command, shell=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())
