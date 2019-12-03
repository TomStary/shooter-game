import sys
import os

from random import random

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

import strategies
from commands import Command
from config import config

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
        self._base = BaseInfo(1, 0, 5, 0, strategies.ballistic)
        self._birds = []
        self._enemies = []
        self._colisions = []
        self._commands = []
        self._cannon = None
        self._factory = None
        self._time = QTimer()
        self._time.timeout.connect(self.tickUpdate)
        self._time.start(15)

    def tickUpdate(self):
        for command in self._commands.copy():
            command.execute()
            self._commands.remove(command)

        for bird in self._birds.copy():
            bird.move()
            for enemy in self._enemies.copy():
                enemy.move()
                result = enemy.colision(bird, self._factory)
                if result is not None:
                    self._colisions.append(result)
                    self.scoreUp()
                    self._enemies.remove(enemy)
        for enemy in self._colisions.copy():
            if enemy.dying():
                self._colisions.remove(enemy)
        self.notifyMyObservers()

    def setFactory(self, factory):
        self._factory = factory

    def initGame(self):
        self._cannon = self._factory.createCannon(0, 0, self._base.angle, self._base.force, self._base.gravity, self._base._strategy)
        self._enemies.append(self._factory.createEnemy())
        self.notifyMyObservers()

    def acceptVisitor(self, visitor):
        self._cannon.acceptVisitor(visitor)
        for enemy in self._enemies:
            enemy.acceptVisitor(visitor)
        for enemy in self._colisions:
            enemy.acceptVisitor(visitor)
        for bird in self._birds:
            bird.acceptVisitor(visitor)
        self._base.acceptVisitor(visitor)

    def acceptCommand(self, command: Command):
        self._commands.append(command)

    def cannonUp(self):
        self._cannon.moveUp(-5)
        self.notifyMyObservers()

    def cannonDown(self):
        self._cannon.moveDown(5)
        self.notifyMyObservers()

    def angleUp(self, add):
        self._base._angle += add
        self._cannon.aimUp(add)

    def angleDown(self, sub):
        self._base._angle -= sub
        self._cannon.aimDown(sub)

    def forceUp(self, add):
        self._base._force += add
        self._cannon.forceUp(add)

    def forceDown(self, sub):
        self._base._force -= sub
        self._cannon.forceDown(sub)

    def scoreUp(self):
        self._base._score += 1

    def spawnEnemy(self):
        self._enemies.append(self._factory.createEnemy())

    def changeStrategy(self):
        if self._base._strategy == strategies.ballistic:
            self._base._strategy = strategies.oblique
        elif self._base._strategy == strategies.oblique:
            self._base._strategy = strategies.straight
        elif self._base._strategy == strategies.straight:
            self._base._strategy = strategies.ballistic
        self._cannon.setStrategy(self._base.strategy)

    def shoot(self):
        self._birds.append(self._cannon.shoot())
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
    def __init__(self, gravity, score, force, angle, strategy):
        self._gravity = gravity
        self._score = score
        self._force = force
        self._angle = angle
        self._strategy = strategy

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
        self._angle += value

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, val):
        self._strategy = val

    def acceptVisitor(self, visitor):
        visitor.visitGameInfo(self)


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
    def __init__(self, x = 0, y = 0, angle = 0, force = 1, gravity = 0, strategy = None, factory = None):
        super().__init__(25, 69, x, y, "cannon.png")
        self._force = force
        self._angle = angle
        self._gravity = gravity
        self._factory = factory
        self._strategy = strategy

    def moveUp(self, offset_y):
        if self._position.y > 0:
            self.move(0, offset_y)

    def moveDown(self, offset_y):
        self.move(0, offset_y)

    def aimUp(self, offset_angle):
        self._angle += offset_angle

    def aimDown(self, offset_angle):
        self._angle -= offset_angle

    def forceUp(self, add):
        self._force += add

    def forceDown(self, sub):
        self._force -= sub

    def setStrategy(self, strategy):
        self._strategy = strategy

    def shoot(self):
        return self._factory.createBird(self._position, self._angle, self._force, self._gravity, self._strategy)

    def acceptVisitor(self, visitor):
        visitor.visitCannon(self)


class AbstractMissile(PrintableObject):
    def __init__(self, x, y):
        super().__init__(30, 29, x, y, "missile.png")

    def acceptVisitor(self, visitor):
        visitor.visitMissile(self)


class Missile(AbstractMissile):
    def __init__(self, x, y, angle, force, gravity, strategy):
        super().__init__(x, y)
        self._force = force
        self._angle = angle
        self._gravity = gravity
        self._strategy = strategy
        self._distance = 0

    def move(self):
        self._distance += 1
        x, y = self._strategy(self._angle, self._force, self._gravity, self._distance)
        self._position.move(x, y)


class DeadEnemy(PrintableObject):
    def __init__(self, x, y):
        super().__init__(30, 29, x, y, "collision.png")
        self.duration = 50

    def acceptVisitor(self, visitor):
        visitor.visitCollision(self)

    def dying(self):
        self.duration -= 1
        if self.duration > 0:
            return False
        else:
            return True

class AbstractEnemy(PrintableObject):
    def __init__(self, x, y):
        super().__init__(30, 29, x, y, "enemy1.png")

    def colision(self, bird, factory):
        bird_pos = bird.getPosition()
        pig_pos = self.getPosition()
        if (abs(bird_pos.x - pig_pos.x) <= 30) and (abs(bird_pos.y - pig_pos.y) <= 29):
            return factory.createColision(pig_pos)
        else:
            return None

    def acceptVisitor(self, visitor):
        visitor.visitEnemy(self)


class BasicEnemy(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self):
        pass


class MovingEnemy(AbstractEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._vx = random() * 37 % 5
        self._vy = random() * 37 % 5

        a = int(random() * 20) % 2
        b = int(random() * 20) % 2

        if a == 0:
            self._vx *= -1
        if b == 0:
            self._vy *= -1


    def move(self):
        pos = self.getPosition()
        if pos._x + self._vx <= 0 or pos._x + self._vx + self.w  >= config.width:
            self._vx *= -1
        if pos._y + self._vy <= 0 or pos._y + self._vy + self.h  >= config.height:
            self._vy *= -1

        pos._x += self._vx
        pos._y += self._vy

