from logic.sca import SCAActuator
from .mixins import Bindable


class MotionActuator(SCAActuator, Bindable):

    def __init__(self, name):
        super(MotionActuator, self).__init__(name)

        self.translation = (0, 0, 0)

    def on_update(self):
        x, y, z = self.object.getPos()
        dx, dy, dz = self.translation
        self.object.setPos(x + dx, y + dy, z + dz)