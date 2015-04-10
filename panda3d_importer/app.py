from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from json import loads
from python_importer import SCALogicImporter

from .actuators import MotionActuator
from .sensors import KeyboardSensor
from .mixins import Bindable


json_logic = '''{"actuators": [{"angular_velocity": [0.0, 0.0, 0.0], "show_expanded": false, "use_local_rotation": true, "force_min_x": 0.0, "use_local_location": true, "force_max_y": 0.09999999403953552, "force_min_z": 0.0, "force_min_y": 0.0, "use_servo_limit_z": true, "type": "MOTION", "linear_velocity": [0.0, 0.0, 0.0], "integral_coefficient": 0.0, "torque": [0.0, 0.0, 0.0], "use_local_torque": true, "use_local_angular_velocity": false, "name": "Mouse", "offset_location": [0.0, 0.09999999403953552, 0.0], "proportional_coefficient": 0.0, "derivate_coefficient": 0.0, "pin": false, "active": true, "damping": 0, "use_local_force": true, "mode": "OBJECT_NORMAL", "force_max_z": 0.0, "force_max_x": 0.0, "force": [0.0, 0.0, 0.0], "use_local_linear_velocity": false, "use_servo_limit_y": true, "use_add_linear_velocity": false, "use_add_character_location": false, "use_character_jump": false, "use_servo_limit_x": true}, {"angular_velocity": [0.0, 0.0, 0.0], "show_expanded": false, "use_local_rotation": true, "force_min_x": 0.0, "use_local_location": true, "force_max_y": -0.09999999403953552, "force_min_z": 0.0, "force_min_y": 0.0, "use_servo_limit_z": true, "type": "MOTION", "linear_velocity": [0.0, 0.0, 0.0], "integral_coefficient": 0.0, "torque": [0.0, 0.0, 0.0], "use_local_torque": true, "use_local_angular_velocity": false, "name": "Message", "offset_location": [0.0, -0.09999999403953552, 0.0], "proportional_coefficient": 0.0, "derivate_coefficient": 0.0, "pin": false, "active": true, "damping": 0, "use_local_force": true, "mode": "OBJECT_NORMAL", "force_max_z": 0.0, "force_max_x": 0.0, "force": [0.0, 0.0, 0.0], "use_local_linear_velocity": false, "use_servo_limit_y": true, "use_add_linear_velocity": false, "use_add_character_location": false, "use_character_jump": false, "use_servo_limit_x": true}, {"angular_velocity": [0.0, 0.0, 0.0], "show_expanded": false, "use_local_rotation": true, "force_min_x": 0.0, "use_local_location": true, "force_max_y": 0.0, "force_min_z": 0.0, "force_min_y": 0.0, "use_servo_limit_z": true, "type": "MOTION", "linear_velocity": [0.0, 0.0, 0.0], "integral_coefficient": 0.0, "torque": [0.0, 0.0, 0.0], "use_local_torque": true, "use_local_angular_velocity": false, "name": "Message1", "offset_location": [-0.09999999403953552, 0.0, 0.0], "proportional_coefficient": 0.0, "derivate_coefficient": 0.0, "pin": false, "active": true, "damping": 0, "use_local_force": true, "mode": "OBJECT_NORMAL", "force_max_z": 0.0, "force_max_x": -0.09999999403953552, "force": [0.0, 0.0, 0.0], "use_local_linear_velocity": false, "use_servo_limit_y": true, "use_add_linear_velocity": false, "use_add_character_location": false, "use_character_jump": false, "use_servo_limit_x": true}, {"angular_velocity": [0.0, 0.0, 0.0], "show_expanded": true, "use_local_rotation": true, "force_min_x": 0.0, "use_local_location": true, "force_max_y": 0.0, "force_min_z": 0.0, "force_min_y": 0.0, "use_servo_limit_z": true, "type": "MOTION", "linear_velocity": [0.0, 0.0, 0.0], "integral_coefficient": 0.0, "torque": [0.0, 0.0, 0.0], "use_local_torque": true, "use_local_angular_velocity": false, "name": "Message2", "offset_location": [0.09999999403953552, 0.0, 0.0], "proportional_coefficient": 0.0, "derivate_coefficient": 0.0, "pin": false, "active": true, "damping": 0, "use_local_force": true, "mode": "OBJECT_NORMAL", "force_max_z": 0.0, "force_max_x": 0.09999999403953552, "force": [0.0, 0.0, 0.0], "use_local_linear_velocity": false, "use_servo_limit_y": true, "use_add_linear_velocity": false, "use_add_character_location": false, "use_character_jump": false, "use_servo_limit_x": true}], "controllers": [{"active": true, "show_expanded": true, "states": 1, "actuators": ["Mouse"], "type": "LOGIC_AND", "use_priority": false, "name": "And"}, {"active": true, "show_expanded": true, "states": 1, "actuators": ["Message"], "type": "LOGIC_AND", "use_priority": false, "name": "And1"}, {"active": true, "show_expanded": true, "states": 1, "actuators": ["Message1"], "type": "LOGIC_AND", "use_priority": false, "name": "And2"}, {"active": true, "show_expanded": true, "states": 1, "actuators": ["Message2"], "type": "LOGIC_AND", "use_priority": false, "name": "And3"}, {"active": true, "show_expanded": true, "states": 1, "actuators": [], "type": "LOGIC_XNOR", "use_priority": false, "name": "Python"}], "sensors": [{"modifier_key_2": "NONE", "log": "", "show_expanded": false, "modifier_key_1": "NONE", "pin": false, "target": "", "use_pulse_true_level": false, "use_level": false, "key": "W", "use_tap": false, "invert": false, "active": true, "type": "KEYBOARD", "use_all_keys": false, "frequency": 0, "use_pulse_false_level": false, "controllers": ["And"], "name": "Always1"}, {"modifier_key_2": "NONE", "log": "", "show_expanded": false, "modifier_key_1": "NONE", "pin": false, "target": "", "use_pulse_true_level": false, "use_level": false, "key": "S", "use_tap": false, "invert": false, "active": true, "type": "KEYBOARD", "use_all_keys": false, "frequency": 0, "use_pulse_false_level": false, "controllers": ["And1"], "name": "Keyboard"}, {"modifier_key_2": "NONE", "log": "", "show_expanded": false, "modifier_key_1": "NONE", "pin": false, "target": "", "use_pulse_true_level": false, "use_level": false, "key": "A", "use_tap": false, "invert": false, "active": true, "type": "KEYBOARD", "use_all_keys": false, "frequency": 0, "use_pulse_false_level": false, "controllers": ["And2"], "name": "Keyboard1"}, {"modifier_key_2": "NONE", "log": "", "show_expanded": true, "modifier_key_1": "NONE", "pin": false, "target": "", "use_pulse_true_level": false, "use_level": false, "key": "D", "use_tap": false, "invert": false, "active": true, "type": "KEYBOARD", "use_all_keys": false, "frequency": 0, "use_pulse_false_level": false, "controllers": ["And3"], "name": "Keyboard2"}]}'''
connection_data = loads(json_logic)


class PandaLogicImporter(SCALogicImporter):

    def __init__(self, data, obj):
        super(PandaLogicImporter, self). __init__(data)

        # Bind bindable sensors
        for sensor in self.sensors.values():
            if isinstance(sensor, Bindable):
                sensor.bind(obj)

        # Bind bindable actuators
        for actuator in self.actuators.values():
            if isinstance(actuator, Bindable):
                actuator.bind(obj)

    def _build_event_manager(self, data):
        self.actuator_builders.update({'MOTION': self.build_motion})
        self.sensor_builders.update({'KEYBOARD': self.build_keyboard})

        return super(PandaLogicImporter, self)._build_event_manager(data)

    def build_keyboard(self, sensor_data):
        name = sensor_data['name']

        sensor = KeyboardSensor(name)

        sensor.key = sensor.get_panda_key_name(sensor_data['key'])
        sensor.modifier_1 = sensor.get_panda_key_name(sensor_data['modifier_key_1'])
        sensor.modifier_2 = sensor.get_panda_key_name(sensor_data['modifier_key_2'])
        sensor.use_all_keys = sensor_data['use_all_keys']

        self.populate_sensor_attributes(sensor, sensor_data)

        return sensor

    def build_motion(self, actuator_data):
        name = actuator_data['name']

        actuator = MotionActuator(name)
        actuator.translation = actuator_data['offset_location']

        self.populate_actuator_attributes(actuator, actuator_data)

        return actuator


class LogicManager(object):

    def __init__(self):
        self.accumulator = 0.0
        self.tick_rate = 60

        self.on_tick = None

    def update(self, delta_time):
        self.accumulator += delta_time

        dt = 1. / self.tick_rate

        while self.accumulator >= dt:
            if callable(self.on_tick):
                self.on_tick()

            self.accumulator -= dt


class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

        self.event_managers = []

        self.logic_manager = LogicManager()
        self.logic_manager.on_tick = self.update_event_managers

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.update_logic_manager, "update")
        self._last_time = 0

        self.create_test_object()

    # Define a procedure to move the camera.
    def update_logic_manager(self, task):
        dt = task.time - self._last_time
        self._last_time = task.time
        self.logic_manager.update(dt)
        return Task.cont

    def update_event_managers(self):
        for event_manager in self.event_managers:
            event_manager.update()

    def create_test_object(self):
        # Load the environment model.
        obj = self.loader.loadModel("../panda3d_importer/cube")

        # Reparent the model to render.
        obj.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        obj.setPos(0, 100, 0)

        # Load logic bricks
        event_manager = PandaLogicImporter(connection_data, obj).event_manager
        self.event_managers.append(event_manager)


def start():
    app = MyApp()
    base.world = app
    app.run()