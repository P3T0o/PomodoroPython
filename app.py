import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()

    def initUI(self):
        self.setWindowTitle("Minuteur PyQt")
        self.layout = QVBoxLayout()
        self.label = QLabel("0")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)  # Le minuteur se déclenche toutes les 1000 ms (1 seconde)
        self.seconds = 0

    def updateTimer(self):
        self.seconds += 1
        self.label.setText(f"{self.seconds} secondes")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())