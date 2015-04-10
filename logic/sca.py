class SCAMember(object):

    def __init__(self, name):
        self.name = name

    def _connect(self, other):
        pass

    def connect_to(self, other):
        self._connect(other)
        other._connect(self)


class SCASensor(SCAMember):
    """Base class for sensors"""

    def __init__(self, name):
        super(SCASensor, self).__init__(name)

        self.controllers = []

        self.use_positive_pulse = False
        self.use_negative_pulse = False

        self.invert_output = False
        self.use_tap = False
        self.use_level = True

        self.positive = False
        self.triggered = False

        self._pulse_frequency = 0
        self._positive_count = 0
        self._negative_count = 0

    def _connect(self, other):
        if not isinstance(other, SCAController):
            raise TypeError("Expected SCAController instance")

        self.controllers.append(other)

    @property
    def pulse_frequency(self):
        return self._pulse_frequency

    @pulse_frequency.setter
    def pulse_frequency(self, frequency):
        self._pulse_frequency = frequency
        self._negative_count = frequency
        self._positive_count = frequency

    @property
    def desires_positive_trigger(self):
        return False

    @property
    def desires_positive_state(self):
        return self.invert_output

    def evaluate(self):
        previous_state = self.positive
        requires_trigger = self.desires_positive_trigger
        state = self.desires_positive_state

        if requires_trigger:
            # Already had a trigger, so don't trigger further
            if not state and self.use_tap:
                requires_trigger = False

        else:
            if self.use_positive_pulse:
                self._positive_count += 1

                # We're going to trigger, so reset
                if self._positive_count > self.pulse_frequency:
                    requires_trigger = True

                    self._positive_count = 0
                    self._negative_count = 0

                else:
                    requires_trigger = False

            # Ignore tap in negative mode`
            elif self.use_negative_pulse and not self.use_tap:
                self._negative_count += 1

                # We're going to trigger, so reset
                if not self._negative_count > self.pulse_frequency:
                    requires_trigger = True

                    self._negative_count = 0
                    self._positive_count = 0

                else:
                    requires_trigger = False

        # If tap is enabled, and this is the frame after a trigger
        if self.use_tap and not requires_trigger:
            # Send a trigger if we need are changing state
            if previous_state:
                requires_trigger = True

            # But set state to negative
            state = False

        self.positive = state
        return requires_trigger


class SCAController(SCAMember):
    """Base class for controllers"""

    def __init__(self, name):
        super(SCAController, self).__init__(name)

        self.sensors = []
        self.actuators = []

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

    def set_all_actuators(self, state):
        for actuator in self.actuators:
            actuator.active = state


class SCAActuator(SCAMember):
    """Base class for actuators"""

    def __init__(self, name):
        super(SCAActuator, self).__init__(name)

        self.controllers = []

        self.active = False

    def _connect(self, other):
        if not isinstance(other, SCAController):
            raise TypeError("Expected SCAController instance")

        self.controllers.append(other)

    def on_update(self):
        pass