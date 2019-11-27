"""
Author: Tomas Stary
E-mail: staryto5@fit.cvut.cz
"""


import sys
import os

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication


APP_ROOT = os.path.abspath(os.path.join(__file__, '..'))
qt_creator_file = f'{APP_ROOT}/ui/mainWindow.ui'
UiMainWindow, _ = uic.loadUiType(qt_creator_file)


class Canvas(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.setFocusPolicy(Qt.ClickFocus)

    def paintEvent(self, event: QPaintEvent):
        self._controller.print_bird()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:
            self._controller.move_cannon(0, -10)
        elif event.key() == Qt.Key_Down:
            self._controller.move_cannon(0, 10)
        elif event.key() == Qt.Key_Space:
            self._controller.shoot();


class PrintableObject:
    def __init__(self, w, h, x, y, pic):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.pic = QPixmap(f'{APP_ROOT}/ui/assets/{pic}')


class Bird(PrintableObject):
    def __init__(self, w, h, x, y):
        super(Bird, self).__init__(w, h, x, y, "missile.png")
        self._fired = False

    @property
    def fired(self):
        return self._fired

    @fired.setter
    def fired(self, val):
        self._fired = val


class Cannon(PrintableObject):
    def __init__(self, w, h, x, y):
        super(Cannon, self).__init__(w, h, x, y, "cannon.png")


class Printer:
    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def print_object(self, object: PrintableObject):
        painter = QPainter(self._canvas)
        painter.drawPixmap(object.x, object.y, object.w, object.h, object.pic)


class Controller:
    def __init__(self):
        self.canvas = Canvas(self)
        self.printer = Printer(self.canvas)
        self.projectiles = []
        for i in range(0,10):
            self.projectiles.append(Bird(30, 29, 0, 0))
        self.cannon = Cannon(25, 69, 0, 0)
        self.timer = QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.animation)

    def print_bird(self):
        self.printer.print_object(self.cannon)
        for projectile in self.projectiles:
            self.printer.print_object(projectile)

    def move_cannon(self, offset_x: int, offset_y: int):
        self.cannon.x += offset_x
        self.cannon.y += offset_y
        self.canvas.update()

    def shoot(self):
        print("fire")
        for projectile in self.projectiles:
            if not projectile.fired:
                projectile.fired = True
                break;
        if not self.timer.isActive():
            self.timer.start()

    def animation(self):
        for projectile in self.projectiles:
           if projectile.fired:
            projectile.x += 1
        self.canvas.update()


class AppWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        UiMainWindow.__init__(self)
        self.setupUi(self)

        controller = Controller()

        canvas_holder = self.findChild(QScrollArea, 'canvasHolder')
        canvas_holder.setWidget(controller.canvas)
        canvas_holder.setStyleSheet('background-color: white')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()

    # Wrapping the GUI execution into `sys.exit()` to ensure that proper result code
    # will be returned when the window closes (otherwise it's always 0)
    sys.exit(app.exec_())
