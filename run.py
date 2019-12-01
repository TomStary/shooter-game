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

from models import GameModel, ProxyGameModel, Observer


APP_ROOT = os.path.abspath(os.path.join(__file__, '..'))
qt_creator_file = f'{APP_ROOT}/ui/mainWindow.ui'
UiMainWindow, _ = uic.loadUiType(qt_creator_file)


class Canvas(QWidget):
    def __init__(self, controller):
        super().__init__()
        self._controller = controller
        self.setFocusPolicy(Qt.ClickFocus)

    def paintEvent(self, event: QPaintEvent): #TODO rework rendering
        pass

    def keyPressEvent(self, event: QKeyEvent):
        self._controller.handleKeyCode(event.key())

# class Printer:
#     def __init__(self, canvas: Canvas):
#         self._canvas = canvas

#     def print_object(self, object: PrintableObject):
#         painter = QPainter(self._canvas)
#         painter.drawPixmap(object.x, object.y, object.w, object.h, object.pic)


class Controller:
    def __init__(self, gameModel:GameModel):
        self.gameModel = ProxyGameModel(gameModel)

class AppWindow(QMainWindow, UiMainWindow):
    def __init__(self, controller):
        QMainWindow.__init__(self)
        UiMainWindow.__init__(self)
        self.setupUi(self)

        self.canvas = Canvas(controller)

        canvas_holder = self.findChild(QScrollArea, 'canvasHolder')
        canvas_holder.setWidget(self.canvas)
        canvas_holder.setStyleSheet('background-color: white')


class GameView(Observer):
    def __init__(self, controller):
        self._platform = AppWindow(controller)

    def init(self):
        self._platform.show()
        self.forceLabel = self._platform.findChild(QLabel, 'forceLabel')
        self.angleLabel = self._platform.findChild(QLabel, 'angleLabel')
        self.gravityLabel = self._platform.findChild(QLabel, 'gravityLabel')
        self.scoreLabel = self._platform.findChild(QLabel, 'scoreLabel')

    def update(self):
        pass


class GameRenderer(Visitor):


class ShooterGame:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gameModel = GameModel()
        self.controller = Controller(self.gameModel)
        self.view = GameView(self.controller)
        self.gameModel.registerObserver(view)
        self.view.init(self.gameModel)

        sys.exit(self.app.exec_())


if __name__ == '__main__':
    ShooterGame()
