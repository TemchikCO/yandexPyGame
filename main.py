import sys

from random import randrange

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QSlider



class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.do_paint = False
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.paint)

    def paint(self):
        self.do_paint = True
        self.repaint()

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.smile(qp)
            qp.end()

    def smile(self, qp):
        qp.setBrush(QColor(255, 255, 0))
        x = randrange(300)
        qp.drawEllipse(100, 100, x, x)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
