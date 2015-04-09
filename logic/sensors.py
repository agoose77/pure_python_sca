from .sca import SCASensor


class AlwaysSensor(SCASensor):

    def __init__(self, name):
        super().__init__(name)

        self._trigger = True

    @property
    def desires_positive_trigger(self):
        result = self._trigger
        self._trigger = False
        return result

    @property
    def desires_positive_state(self):
        return not self.invert_output