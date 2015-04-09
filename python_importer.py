from collections import OrderedDict

from logic.sensors import AlwaysSensor
from logic.controllers import PythonScriptController, PythonModuleController, ANDController
from logic.event_manager import SCAEventManager


class SCALogicImporter(object):

    def __init__(self, data):
        self.sensors = OrderedDict()
        self.controllers = OrderedDict()
        self.actuators = OrderedDict()

        self.sensor_builders = dict(ALWAYS=self.build_always)
        self.controller_builders = dict(PYTHON=self.build_python, LOGIC_AND=self.build_and)
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
        actuator_builders = self.actuator_builders
        for actuator_data in data['actuators']:
            actuator_type = actuator_data['type']
            actuator_name = actuator_data['name']

            actuator_builder = actuator_builders[actuator_type]
            actuator = actuator_builder(actuator_data)

            actuators[actuator_name] = actuator

        for get_x, get_y in self.pending_connections:
            try:
                x = get_x()
                y = get_y()

                x.connect_to(y)

            except KeyError as err:
                print("Connection failed", err)

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

    def populate_sensor_attributes(self, sensor, sensor_data):
        sensor.use_positive_pulse = sensor_data['use_pulse_true_level']
        sensor.use_negative_pulse = sensor_data['use_pulse_false_level']
        sensor.use_tap = sensor_data['use_tap']
        sensor.invert_output = sensor_data['invert']

        pending_connections = self.pending_connections
        for controller_name in sensor_data['controllers']:
            get_sensor = lambda: sensor
            get_controller = self.deferred_get_controller(controller_name)

            pending_connections.append((get_sensor, get_controller))

    def populate_controller_attributes(self, controller, controller_data):
        pending_connections = self.pending_connections
        for controller_name in controller_data['actuators']:
            get_controller = lambda: controller
            get_actuator = self.deferred_get_actuator(controller_name)

            pending_connections.append((get_controller, get_actuator))

    def populate_actuator_attributes(self, actuator, actuator_data):
        pass

    def build_and(self, controller_data):
        name = controller_data['name']
        controller = ANDController(name)

        self.populate_controller_attributes(controller, controller_data)

        return controller

    def build_always(self, sensor_data):
        name = sensor_data['name']
        sensor = AlwaysSensor(name)

        self.populate_sensor_attributes(sensor, sensor_data)

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

        self.populate_controller_attributes(controller, controller_data)

        return controller


