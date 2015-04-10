from .sca import SCASensor


class AlwaysSensor(SCASensor):

    def __init__(self, name):
        super(AlwaysSensor, self).__init__(name)

        self._trigger = True

    @property
    def desires_positive_trigger(self):
        result = self._trigger
        self._trigger = False
        return result

    @property
    def desires_positive_state(self):
        return not self.invert_output


class DelaySensor(SCASensor):

    def __init__(self, name):
        super(DelaySensor, self).__init__(name)

        self.delay = 0
        self.duration = 0

    @property
    def desires_positive_trigger(self):
        result = not self.delay or not self.duration
        self.delay -= 1
        self.duration -= 1
        return result

    @property
    def desires_positive_state(self):
        state = not self.delay
        if self.invert_output:
            state = not state

        return state