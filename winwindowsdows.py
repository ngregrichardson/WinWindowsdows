import sys

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np


class CustomWindow(QMainWindow):
    def paintEvent(self, event=None):
        painter = QPainter(self)
        size = 50
        image = QImage('res.png') # TODO add default image
        if not image.isNull():
            painter.setOpacity(0.0)
            painter.setBrush(Qt.white)
            painter.setPen(QPen(Qt.white))
            painter.drawRect(self.rect())
            painter.setOpacity(1.0)
            painter.begin(image)
            painter.drawImage(self.rect(), image)
            painter.setBrush(Qt.white)
            painter.setPen(QPen(Qt.white))
            painter.drawRect(0, self.frameGeometry().height() / 2 - size / 2, self.frameGeometry().width(), size)
            painter.drawRect(self.frameGeometry().width() / 2 - size / 2, 0, size, self.frameGeometry().height())


def show_webcam(win, mirror=True):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        alpha = np.full_like(img[..., 0], 5)
        bgra = cv2.merge((img, alpha))
        cv2.imwrite('res.png', bgra)
        win.repaint()
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()

app = QApplication(sys.argv)

# Create the main window
window = CustomWindow()

window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)

# Run the application
window.showFullScreen()
show_webcam(window)
sys.exit(app.exec_())