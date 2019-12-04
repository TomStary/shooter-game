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

from models import GameModel, Observer, Visitor, BaseInfo
from factory import GameFactoryArcade, GameFactoryRealistic
from state import State
import commands
from config import config


APP_ROOT = os.path.abspath(os.path.join(__file__, '..'))
qt_creator_file = f'{APP_ROOT}/ui/mainWindow.ui'
UiMainWindow, _ = uic.loadUiType(qt_creator_file)


class Canvas(QWidget):
    def __init__(self, controller, model, view):
        super().__init__()
        self._controller = controller
        self._model = model
        self._view = view
        self.setFocusPolicy(Qt.ClickFocus)

    def paintEvent(self, event: QPaintEvent):
        self._model.acceptVisitor(self._view.renderer)

    def keyPressEvent(self, event: QKeyEvent):
        self._controller.handleKeyCode(event.key())


class Controller:
    def __init__(self, gameModel:GameModel):
        self.gameModel = gameModel

    def handleKeyCode(self, keyCode):
        if keyCode == Qt.Key_Up:
            self.gameModel.acceptCommand(commands.CannonUpCommand(self.gameModel))
        elif keyCode == Qt.Key_Down:
            self.gameModel.acceptCommand(commands.CannonDownCommand(self.gameModel))
        elif keyCode == Qt.Key_Space:
            self.gameModel.acceptCommand(commands.ShootCommand(self.gameModel))
        elif keyCode == Qt.Key_W:
            self.gameModel.acceptCommand(commands.AngleUpCommand(self.gameModel))
        elif keyCode == Qt.Key_S:
            self.gameModel.acceptCommand(commands.AngleDownCommand(self.gameModel))
        elif keyCode == Qt.Key_R:
            self.gameModel.acceptCommand(commands.ForceUpCommand(self.gameModel))
        elif keyCode == Qt.Key_F:
            self.gameModel.acceptCommand(commands.ForceDownCommand(self.gameModel))
        elif keyCode == Qt.Key_G:
            self.gameModel.acceptCommand(commands.ChangeStrategyCommand(self.gameModel))
        elif keyCode == Qt.Key_P:
            self.gameModel.acceptCommand(commands.SpawnEnemyCommand(self.gameModel))
        elif keyCode == Qt.Key_N:
            self.gameModel.acceptCommand(commands.SaveCommand(self.gameModel))
        elif keyCode == Qt.Key_M:
            self.gameModel.acceptCommand(commands.LoadCommand(self.gameModel))
        elif keyCode == Qt.Key_O:
            self.gameModel.acceptCommand(commands.ChangeModeCommand(self.gameModel))


class AppWindow(QMainWindow, UiMainWindow):
    def __init__(self, controller, model, view):
        QMainWindow.__init__(self)
        UiMainWindow.__init__(self)
        self.setupUi(self)

        self.canvas = Canvas(controller, model, view)

        canvas_holder = self.findChild(QScrollArea, 'canvasHolder')
        canvas_holder.setWidget(self.canvas)
        canvas_holder.setStyleSheet('background-color: white')


class GameView(Observer):
    def __init__(self, controller, model):
        self._platform = AppWindow(controller, model, self)
        self._model = model
        self.renderer = GameRenderer(self._platform)
        self._platform.show()

    def update(self):
        self.renderer.update()


class Printer:
    def draw(self, object):
        pass


class QtPrinter(Printer):
    def __init__(self, canvas):
        self._canvas = canvas
    def draw(self, entity):
        painter = QPainter(self._canvas)
        #this might need some tinkering
        position = entity.getPosition()
        painter.drawPixmap(position.x, position.y, entity.w, entity.h, entity.pic)


class GameRenderer(Visitor):
    def __init__(self, platform):
        self._forceLabel = platform.findChild(QLabel, 'forceLabel')
        self._angleLabel = platform.findChild(QLabel, 'angleLabel')
        self._gravityLabel = platform.findChild(QLabel, 'gravityLabel')
        self._scoreLabel = platform.findChild(QLabel, 'scoreLabel')
        self._canvas = platform.canvas
        self._printer = QtPrinter(self._canvas)

    def draw(self, entity):
       self._printer.draw(entity)

    def update(self):
        self._canvas.update()

    def setForce(self, force):
        self._forceLabel.setText(f"Force: {force}")

    def setAngle(self, angle):
        self._angleLabel.setText(f"Angle: {angle}")

    def setGravity(self, gravity):
        self._gravityLabel.setText(f"Gravity: {gravity}")

    def setScore(self, score):
        self._scoreLabel.setText(f"Score: {score}")

    def visitCannon(self, cannon):
        self.draw(cannon)

    def visitMissile(self, missile):
        self.draw(missile)

    def visitEnemy(self, enemy):
        self.draw(enemy)

    def visitCollision(self, enemy):
        self.draw(enemy)

    def visitGameInfo(self, info: BaseInfo):
        self.setAngle(info.angle)
        self.setForce(info.force)
        self.setGravity(info.gravity)
        self.setScore(info.score)


class ShooterGame:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.state = State()
        self.gameModel = GameModel()
        self.controller = Controller(self.gameModel)
        self.view = GameView(self.controller, self.gameModel)
        self.gameModel.registerObserver(self.view)
        self.gameModel.setFactory()
        self.gameModel.initGame()

        sys.exit(self.app.exec_())


if __name__ == '__main__':
    ShooterGame()
