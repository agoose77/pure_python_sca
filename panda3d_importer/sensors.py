from direct.showbase import DirectObject
from logic.sca import SCASensor


MODIFIER_ORDER = "shift", "control", "alt"


def sort_modifiers(modifiers):
    def sort_key(item):
        if item in MODIFIER_ORDER:
            return len(MODIFIER_ORDER) - MODIFIER_ORDER.index(item)

        return -1

    modifiers.sort(key=sort_key, reverse=True)


class SCAEventSensor(SCASensor):

    def __init__(self, name):
        super(SCAEventSensor, self).__init__(name)

        self._received_event = False
        self._event_just_changed = False

        self._listener = DirectObject.DirectObject()

    @property
    def desires_positive_trigger(self):
        do_trigger = self._event_just_changed
        self._event_just_changed = False
        return do_trigger

    @property
    def desires_positive_state(self):
        return self._received_event

    def _on_event_down(self):
        self._received_event = True
        self._event_just_changed = True

    def _on_event_up(self):
        self._received_event = False
        self._event_just_changed = True


class KeyboardSensor(SCAEventSensor):

    def __init__(self, name):
        super(KeyboardSensor, self).__init__(name)

        self._listen_keys = []

        self._key = None
        self._modifier_1 = None
        self._modifier_2 = None

        self.use_all_keys = False

        self._active_buttons = set()

    @staticmethod
    def get_panda_event_name(name, left_right_unique=True):
        if name == "NONE":
            return None

        name = name.lower().replace("_", "").replace("ctrl", "control")

        if left_right_unique:
            name = name.replace("left", "l").replace("right", "r")
        else:
            name = name.replace("left", "").replace("right", "")

        return name

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
        self._update_listeners()

    @property
    def modifier_1(self):
        return self.modifier_1

    @modifier_1.setter
    def modifier_1(self, key):
        self._modifier_1 = key
        self._update_listeners()

    @property
    def modifier_2(self):
        return self.modifier_2

    @modifier_2.setter
    def modifier_2(self, key):
        self._modifier_2 = key
        self._update_listeners()

    def _update_listeners(self):
        self._listener.ignoreAll()

        keys = []
        if self._modifier_2:
            keys.append(self._modifier_2)

        if self._modifier_1:
            keys.append(self._modifier_1)

        sort_modifiers(keys)

        if self._key:
            keys.append(self._key)

        event_name = "-".join(keys)

        # Bind keys
        if keys:
            self._listener.accept(event_name, self._on_event_down)
            self._listener.accept("buttonUp", self._on_button_up)
            self._listener.accept("buttonDown", self._on_button_down)

        # Record the keys we listen for
        self._listen_keys = keys

    def _on_button_down(self, event):
        for btn in event.split("-"):
            self._active_buttons.add(btn)

        if self.use_all_keys:
            self._on_event_down()

    def _on_button_up(self, btn):
        self._active_buttons.remove(btn)

        if self.use_all_keys:
            if not self._active_buttons:
                self._on_event_up()

        elif btn in self._listen_keys:
            self._on_event_up()


class MouseSensor(SCAEventSensor):
    EVENT_NAMES = {"LEFTCLICK": "mouse1", "MIDDLECICK": "mouse2", "RIGHTCLICK": "mouse3",
                   "WHEELUP": "wheel_up", "WHEELDOWN": "wheel_down"}

    def __init__(self, name):
        super(MouseSensor, self).__init__(name)

        self._mouse_event = None

    @property
    def mouse_event(self):
        return self._mouse_event

    @mouse_event.setter
    def mouse_event(self, event):
        self._mouse_event = event

        self._listener.ignoreAll()
        self._listener.accept(event, self._on_event_down)
        self._listener.accept("{}-up".format(event), self._on_event_up)

    @classmethod
    def get_panda_event_name(cls, name):
        return cls.EVENT_NAMES[name]