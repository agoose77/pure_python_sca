from sca import SCASensor, SCAController, SCAActuator
from event_manager import SCAEventManager

from functools import partial
from inspect import getargspec


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


class AlwaysSensor(SCASensor):

    def __init__(self, name):
        super().__init__(name)

        self._has_triggered = False

    def evaluate(self):
        self.positive = True


converted = '''{"controllers": [{"states": 1, "type": "PYTHON", "mode": "MODULE", "name": "Python", "use_debug": false, "show_expanded": true, "use_priority": false, "actuators": [], "active": true, "module": "test_module.main"}], "actuators": [], "sensors": [{"invert": false, "type": "ALWAYS", "controllers": ["Python"], "name": "Always1", "frequency": 0, "use_tap": false, "use_pulse_true_level": false, "use_pulse_false_level": false, "active": true, "pin": false, "show_expanded": true, "use_level": false}]}'''


from collections import OrderedDict


class Builder:

    def __init__(self, data):
        self.sensors = OrderedDict()
        self.controllers = OrderedDict()
        self.actuators = OrderedDict()

        self.sensor_builders = dict(ALWAYS=self.build_always)
        self.controller_builders = dict(PYTHON=self.build_python)
        self.actuator_builders = dict()

        self.pending_connections = []

        self.event_manager = self._build_event_manager(data)

    def _build_event_manager(self, data):
        sensors = self.sensors
        sensor_builders = self.sensor_builders
        for sensor_data in data['sensors']:
            sensor_type = sensor_data['type']
            sensor_name = sensor_data['name']

            sensor_builder = sensor_builders[sensor_type]
            sensor = sensor_builder(sensor_data)

            sensors[sensor_name] = sensor

        controllers = self.controllers
        controller_builders = self.controller_builders
        for controller_data in data['controllers']:
            controller_type = controller_data['type']
            controller_name = controller_data['name']

            controller_builder = controller_builders[controller_type]
            controller = controller_builder(controller_data)

            controllers[controller_name] = controller

        actuators = self.actuators
        actuator_builders = self.controller_builders
        for actuator_data in data['actuators']:
            actuator_type = actuator_data['type']
            actuator_name = actuator_data['name']

            actuator_builder = actuator_builders[actuator_type]
            actuator = actuator_builder(actuator_data)

            actuators[actuator_name] = actuator

        for get_x, get_y in self.pending_connections:
            x = get_x()
            y = get_y()

            x.connect_to(y)

        event_manager = SCAEventManager()

        event_manager.sensors = list(sensors.values())
        event_manager.controllers = list(controllers.values())
        event_manager.actuators = list(actuators.values())

        return event_manager

    def deferred_get_sensor(self, name):
        def getter():
            return self.sensors[name]
        return getter

    def deferred_get_controller(self, name):
        def getter():
            return self.controllers[name]
        return getter

    def deferred_get_actuator(self, name):
        def getter():
            return self.actuators[name]
        return getter

    def build_always(self, sensor_data):
        name = sensor_data['name']
        sensor = AlwaysSensor(name)

        sensor.use_positive_pulse = sensor_data['use_pulse_true_level']
        sensor.use_negative_pulse = sensor_data['use_pulse_false_level']
        sensor.use_tap = sensor_data['use_tap']

        pending_connections = self.pending_connections
        for controller_name in sensor_data['controllers']:
            get_sensor = lambda: sensor
            get_controller = self.deferred_get_controller(controller_name)

            pending_connections.append((get_sensor, get_controller))

        return sensor

    def build_python(self, controller_data):
        mode = controller_data['mode']
        name = controller_data['name']

        if mode == "MODULE":
            controller = PythonModuleController(name)
            controller.module_string = controller_data['module']

        else:
            controller = PythonScriptController(name)
            controller.script_string = controller_data['text']

        return controller


from json import loads

data = loads(converted)
builder = Builder(data)

event_manager = builder.event_manager

event_manager.update()
event_manager.update()
event_manager.update()
event_manager.update()

# always = AlwaysSensor()
#
# python_module = PythonModuleController()
# python_module.module_string = "test_module.main"
#
# always.connect_to(python_module)
#
# event_manager = SCAEventManager()
# event_manager.sensors.append(always)
#
# event_manager.update()
# event_manager.update()
# event_manager.update()