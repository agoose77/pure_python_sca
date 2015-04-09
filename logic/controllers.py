from inspect import getargspec
from functools import partial


from .sca import SCAController


class ANDController(SCAController):

    def on_triggered(self, sensor):
        state = all([s.positive for s in self.sensors])
        self.set_all_actuators(state)


class NANDController(SCAController):

    def on_triggered(self, sensor):
        state = not all([s.positive for s in self.sensors])
        self.set_all_actuators(state)


class ORController(SCAController):

    def on_triggered(self, sensor):
        state = any([s.positive for s in self.sensors])
        self.set_all_actuators(state)


class NORController(SCAController):

    def on_triggered(self, sensor):
        state = not any([s.positive for s in self.sensors])
        self.set_all_actuators(state)


class XORController(SCAController):

    def on_triggered(self, sensor):
        positive_sensors = [s for s in self.sensors if s.positive]
        state = len(positive_sensors) == 1
        self.set_all_actuators(state)


class XNORController(SCAController):

    def on_triggered(self, sensor):
        previous, *sensors = self.sensors

        state = False
        for sensor in sensors:
            if sensor.positive != previous.positive:
                break
        else:
            state = True

        self.set_all_actuators(state)


class PythonController(SCAController):

    def __init__(self, name):
        super().__init__(name)


class PythonModuleController(PythonController):

    def __init__(self, name):
        super().__init__(name)

        self.module_string = ""
        self._func = None

    @property
    def func(self):
        if self._func is not None:
            return self._func

        *head, tail = self.module_string.split('.')
        module_path = '.'.join(head)

        module = __import__(module_path)
        func = getattr(module, tail)

        if getargspec(func):
            func = partial(func, self)

        self._func = func
        return func

    def on_triggered(self, sensor):
        super().on_triggered(sensor)

        self.func()


class PythonScriptController(PythonController):

    def __init__(self, name):
        super().__init__(name)

        self.script_string = ""

    def on_triggered(self, sensor):
        super().on_triggered(sensor)

        exec(self.script_string)

