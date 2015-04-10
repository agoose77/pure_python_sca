from logic.sca import SCASensor


class KeyboardSensor(SCASensor):

    def __init__(self, name):
        super(KeyboardSensor, self).__init__(name)

        self._key = None
        self._received_event = False
        self._event_just_changed = False

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        if self._key is not None:
            base.ignore("{}-up".format(self._key))
            base.ignore(self._key)

        self._key = key
        base.accept("{}-up".format(key), self._on_event_up)
        base.accept(key, self._on_event_down)

    def _on_event_down(self):
        self._received_event = True
        self._event_just_changed = True

    def _on_event_up(self):
        self._received_event = False
        self._event_just_changed = True

    @property
    def desires_positive_trigger(self):
        do_trigger = self._event_just_changed
        self._event_just_changed = False
        return do_trigger

    @property
    def desires_positive_state(self):
        return self._received_event
