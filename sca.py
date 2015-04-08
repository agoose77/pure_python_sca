class SCAMember:

    def _connect(self, other):
        pass

    def connect_to(self, other):
        self._connect(other)
        other._connect(self)


class SCASensor(SCAMember):
    """Base class for sensors"""

    def __init__(self):
        self.controllers = []

        self.use_positive_pulse = False
        self.use_negative_pulse = False
        self.invert_output = False
        self.use_tap = False
        self.enabled = True

        self.positive = False
        self.triggered = False

    def _connect(self, other):
        if not isinstance(other, SCAController):
            raise TypeError("Expected SCAController instance")

        self.controllers.append(other)

    def evaluate(self):
        pass


class SCAController(SCAMember):
    """Base class for controllers"""

    enabled = True

    def __init__(self):
        self.sensors = []
        self.actuators = []

        self.enabled = True
        self.active = False

    def _connect(self, other):
        if isinstance(other, SCASensor):
            self.sensors.append(other)

        elif isinstance(other, SCAActuator):
            self.actuators.append(other)

        else:
            raise TypeError("Expected SCAActuator or SCASensor instance")

    def on_triggered(self, sensor):
        pass


class SCAActuator(SCAMember):
    """Base class for actuators"""

    def __init__(self):
        self.controllers = []

        self.enabled = True
        self.active = False

    def _connect(self, other):
        if not isinstance(other, SCAController):
            raise TypeError("Expected SCAController instance")

        self.controllers.append(other)

    def on_update(self):
        pass