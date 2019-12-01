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

from models import GameModel, ProxyGameModel


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


class Position:
    def __init__(self, x = 0, y = 0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def move(self, offset_x, offset_y):
        self._x += offset_x
        self._y += offset_y

class PrintableObject():
    def __init__(self, w, h, x, y, pic):
        self.w = w
        self.h = h
        self._position = Position(x, y)
        self.pic = QPixmap(f'{APP_ROOT}/ui/assets/{pic}')

    def getPosition(self):
        return self._position

    def move(self, offset_x, offset_y):
        self._position.move(offset_x, offset_y)


class Bird(PrintableObject):
    def __init__(self, x, y):
        super(Bird, self).__init__(30, 29, x, y, "missile.png")


class Cannon(PrintableObject):
    def __init__(self, x, y):
        super(Cannon, self).__init__(25, 69, x, y, "cannon.png")


class Printer:
    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def print_object(self, object: PrintableObject):
        painter = QPainter(self._canvas)
        painter.drawPixmap(object.x, object.y, object.w, object.h, object.pic)


class Controller:
    def __init__(self, gameModel:GameModel):
        self.gameModel = ProxyGameModel(gameModel)
        self.canvas = Canvas(self)
        self.printer = Printer(self.canvas)
        self.projectiles = []
        self.cannon = Cannon(0, 0)
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
        self.projectiles.append(Bird(self.cannon.x, self.cannon.y))
        self.canvas.update()
        if not self.timer.isActive():
            self.timer.start()

    def animation(self):
        for projectile in self.projectiles:
            projectile.x += 1
            projectile.y += 1
        self.canvas.update()

class AppWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        UiMainWindow.__init__(self)
        self.setupUi(self)

        gameModel = GameModel()
        controller = Controller(gameModel)

        canvas_holder = self.findChild(QScrollArea, 'canvasHolder')
        canvas_holder.setWidget(controller.canvas)
        canvas_holder.setStyleSheet('background-color: white')


class ShooterGame:
    def __init__(self):
        self.app = QApplication(sys.argv)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()

    # Wrapping the GUI execution into `sys.exit()` to ensure that proper result code
    # will be returned when the window closes (otherwise it's always 0)
    sys.exit(app.exec_())
