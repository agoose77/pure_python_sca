from math import degrees
from panda3d.core import Mat4, Vec3, Quat
from logic.sca import SCAActuator

from .mixins import Bindable


def decompose_transform(matrix):
    """Decompose transformation matrix into translation, rotation, scale matrices

    :param matrix: matrix to decompose
    """
    rotation = Mat4()
    matrix.getQuat().extractToMatrix(rotation)

    translation = Mat4().translateMat(matrix.getPos())

    inverse_rotation = Mat4()
    inverse_rotation.invertFrom(rotation)

    inverse_translation = Mat4()
    inverse_translation.invertFrom(translation)

    scale = matrix.getMat() * inverse_translation * inverse_rotation
    return translation, rotation, scale


class MotionActuator(SCAActuator, Bindable):

    MODES = 'OBJECT_CHARACTER', 'OBJECT_NORMAL', 'OBJECT_SERVO'

    def __init__(self, name):
        super(MotionActuator, self).__init__(name)

        self._mode = 'OBJECT_NORMAL'

        self.delta_location = (0, 0, 0)
        self.delta_rotation = (0, 0, 0)

        self.use_local_location = True
        self.use_local_rotation = False

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if not mode in self.__class__.MODES:
            raise ValueError("Invalid mode assigned")

        self._mode = mode

    def update_normal(self):
        position = self.object.getPos()
        orientation = self.object.getQuat()

        displacement = Vec3(*self.delta_location)

        dp, dr, dh = [degrees(a) for a in self.delta_rotation]
        rotation = Vec3(dh, dp, dr)

        rotation_quat = Quat()
        rotation_quat.setHpr(rotation)

        if self.use_local_rotation:
            orientation = rotation_quat * orientation
            print(orientation, "ISORI")

        else:
            orientation *= rotation_quat

        if self.use_local_location:
            position += orientation.xform(displacement)

        else:
            position += displacement

        self.object.setPos(position)
        self.object.setQuat(orientation)

    def update_servo(self):
        pass

    def update_character(self):
        pass

    def on_update(self):
        if self._mode == "OBJECT_NORMAL":
            self.update_normal()

        elif self._mode == "OBJECT_SERVO":
            self.update_servo()

        else:
            self.update_character()