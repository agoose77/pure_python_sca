from sca import SCASensor, SCAController, SCAActuator
from event_manager import SCAEventManager

from functools import partial
from inspect import getargspec


class PythonController(SCAController):

    def __init__(self):
        super().__init__()


class PythonModuleController(PythonController):

    def __init__(self):
        super().__init__()

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

    def __init__(self):
        super().__init__()

        self.script_string = ""

    def on_triggered(self, sensor):
        super().on_triggered(sensor)

        exec(self.script_string)


class AlwaysSensor(SCASensor):

    def __init__(self):
        super().__init__()

        self._has_triggered = False

    def evaluate(self):
        if not self._has_triggered:
            self.positive = True
            self._has_triggered = True
        else:
            self.positive = False


always = AlwaysSensor()

python_module = PythonModuleController()
python_module.module_string = "test_module.main"

always.connect_to(python_module)

event_manager = SCAEventManager()
event_manager.sensors.append(always)

event_manager.update()
event_manager.update()
event_manager.update()