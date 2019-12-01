from PyQt5.QtGui import QPixmap

from run import APP_ROOT

class ProxyGameModel():
    def __init__(self, gameModel:GameModel):
        self.model = gameModel

    def changeModel(self, gravity, score, force, angle):
        #here can be implemented memento for going back and forth with game model - reseting score, undo...
        self.model.angle(angle)
        self.model.gravity(gravity)
        self.model.score(score)
        self.model.force(force)\


class GameModel:
    def __init__(self):
        self._base = BaseInfo(1, 0, 1, 0)


class BaseInfo:
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

class Visitable:
    def __init__(self):
        self.visitors = []

    def acceptVisitor(self, visitor): #TODO: doplnit omezeni na tridu
        self.visitors.append(visitor)

class PrintableObject(Visitor):
    def __init__(self, w, h, x, y, pic):
        self.w = w
        self.h = h
        self._position = Position(x, y)
        self.pic = QPixmap(f'{APP_ROOT}/ui/assets/{pic}')

    def getPosition(self):
        return self._position

    def move(self, offset_x, offset_y):
        self._position.move(offset_x, offset_y)

class AbstractCannon(PrintableObject):
    def __init__(self, x = 0, y = 0, power = 1, angle = 0):
        super().__init__(25, 69, x, y, "cannon.png")
        self._power = power
        self._angle = angle

    def moveUp(self, offset_x):
        self.move(offset_x, 0)

    def moveDown(self, offset_x):
        self.move(offset_x, 0)

    def aimUp(self, offset_angle):
        self._angle += offset_angle

    def aimDown(self, offset_angle):
        self._angle -= offset_angle

    def shoot(self):
        raise NotImplementedError


class AbstractMissile(PrintableObject):
    def __init__(self, x, y):
        super().__init__(30, 29, x, y, "missile.png")


class AbstractEnemy(PrintableObject):
    def __init__(self, x, y, pic):
        super().__init__(30, 29, x, y, pic)
