import sys
import os

from random import random

from PyQt5.QtGui import QPixmap

APP_ROOT = os.path.abspath(os.path.join(__file__, '..'))


class Observer:
    def update(self):
        raise NotImplementedError


class Observable:
    def __init__(self):
        self._observers = []

    def registerObserver(self, observer: Observer):
        self._observers.append(observer)

    def unregisterObserver(self, observer: Observer):
        self._observers.remove(observer)

    def notifyMyObservers(self):
        for observer in self._observers:
            observer.update()

class Visitor:
    def visitCannon(self, cannon):
        pass

    def visitMissile(self, missile):
        pass

    def visitEnemy(self, enemy):
        pass

    def visitGameInfo(self, enemy):
        pass


class Visitable:
    def acceptVisitor(self, visitor: Visitor):
        raise NotImplementedError


class GameModel(Observable, Visitable):
    def __init__(self):
        super().__init__()
        self._base = BaseInfo(1, 0, 1, 0)
        self._birds = []
        self._enemies = []
        self._cannon = None
        self._factory = None

    def setFactory(self, factory):
        self._factory = factory

    def initGame(self):
        self._cannon = self._factory.createCannon(0,0)
        self._enemies.append(self._factory.createEnemy())
        self.notifyMyObservers()

    def acceptVisitor(self, visitor):
        self._cannon.acceptVisitor(visitor)
        for enemy in self._enemies:
            enemy.acceptVisitor(visitor)
        for bird in self._birds:
            bird.acceptVisitor(visitor)
        #self._base.acceptVisitor(visitor)

    def cannonUp(self):
        self._cannon.moveUp(-5)
        self.notifyMyObservers()

    def cannonDown(self):
        self._cannon.moveDown(5)
        self.notifyMyObservers()

    def shoot(self):
        position = self._cannon.getPosition()
        bird = self._factory.createBird(position)
        self._birds.append(bird)
        self.notifyMyObservers()


class ProxyGameModel():
    def __init__(self, gameModel:GameModel):
        self.model = gameModel

    def changeModel(self, gravity, score, force, angle):
        #here can be implemented memento for going back and forth with game model - reseting score, undo...
        self.model.angle(angle)
        self.model.gravity(gravity)
        self.model.score(score)
        self.model.force(force)


class BaseInfo(Visitable):
    #gamemodel should maybe have a snapshot of all enemy positions and also position of canon...
    def __init__(self, gravity, score, force, angle):
        self._gravity = gravity
        self._score = score
        self._force = force
        self._angle = angle

    @property
    def gravity(self):
        return self._gravity

    @gravity.setter
    def gravity(self, value):
        self._gravity = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, value):
        self._force = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    def acceptVisitor(self, visitor):
        pass


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


class PrintableObject(Visitable):
    def __init__(self, w, h, x, y, pic):
        self.w = w
        self.h = h
        self._position = Position(x, y)
        self.pic = QPixmap(f'{APP_ROOT}/ui/assets/{pic}')

    def getPosition(self):
        return self._position

    def move(self, offset_x, offset_y):
        self._position.move(offset_x, offset_y)


class Cannon(PrintableObject):
    def __init__(self, x = 0, y = 0, power = 1, angle = 0):
        super().__init__(25, 69, x, y, "cannon.png")
        self._power = power
        self._angle = angle

    def moveUp(self, offset_y):
        if self._position.y > 0:
            self.move(0, offset_y)

    def moveDown(self, offset_y):
        self.move(0, offset_y)

    def aimUp(self, offset_angle):
        self._angle += offset_angle

    def aimDown(self, offset_angle):
        self._angle -= offset_angle

    def shoot(self):
        raise NotImplementedError

    def acceptVisitor(self, visitor):
        visitor.visitCannon(self)


class AbstractMissile(PrintableObject):
    def __init__(self, x, y):
        super().__init__(30, 29, x, y, "missile.png")

    def acceptVisitor(self, visitor):
        visitor.visitMissile(self)


class Missile(AbstractMissile):
    def __init__(self, x, y):
        super().__init__(x, y)


class AbstractEnemy(PrintableObject):
    def __init__(self, x, y):
        super().__init__(30, 29, x, y, "enemy1.png")

    def acceptVisitor(self, visitor):
        visitor.visitEnemy(self)


class BasicEnemy(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)


class MovingEnemy(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self):
        self._x += 1
        self._y += 1
