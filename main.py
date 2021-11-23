import sys

from random import randrange

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QSlider


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.paint_flag = False
        uic.loadUi('UI.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.paint)

    def paint(self):
        self.paint_flag = True
        self.repaint()

    def paintEvent(self, event):
        if self.paint_flag:
            qp = QPainter()
            qp.begin(self)
            qp.setBrush(QColor(255, 255, 0))
            qp.drawEllipse(randrange(300), randrange(300), 100, 100)
            qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
