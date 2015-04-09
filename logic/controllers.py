from inspect import getargspec
from functools import partial


from .sca import SCAController


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

