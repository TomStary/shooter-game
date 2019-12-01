

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