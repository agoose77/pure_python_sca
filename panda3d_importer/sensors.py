from direct.showbase import DirectObject
from pandac.PandaModules import ModifierButtons, KeyboardButton
from logic.sca import SCASensor


MODIFIER_ORDER = "shift", "control", "alt"


def sort_modifiers(modifiers):
    def sort_key(item):
        if item in MODIFIER_ORDER:
            return len(MODIFIER_ORDER) - MODIFIER_ORDER.index(item)

        return -1

    modifiers.sort(key=sort_key, reverse=True)


class KeyboardSensor(SCASensor):

    def setup(self):
        modifiers = ModifierButtons()

        modifiers.addButton(KeyboardButton.lshift())
        modifiers.addButton(KeyboardButton.rshift())
        modifiers.addButton(KeyboardButton.lcontrol())
        modifiers.addButton(KeyboardButton.rcontrol())
        modifiers.addButton(KeyboardButton.lalt())
        modifiers.addButton(KeyboardButton.ralt())
        modifiers.addButton(KeyboardButton.meta())

        # For supporting "use_all_keys" and modifier keys
        button_node = base.buttonThrowers[0].node()
        button_node.setButtonDownEvent('buttonDown')
        button_node.setButtonUpEvent('buttonUp')
        button_node.setModifierButtons(modifiers)

    def __init__(self, name):
        super(KeyboardSensor, self).__init__(name)

        if not hasattr(self.__class__, "X"):
            self.__class__.X = 1
            self.setup()

        self._listener = DirectObject.DirectObject()
        self._listen_keys = []

        self._key = None
        self._modifier_1 = None
        self._modifier_2 = None

        self.use_all_keys = False

        self._received_event = False
        self._event_just_changed = False

        self._active_buttons = set()

    @staticmethod
    def get_panda_key_name(name, left_right_unique=True):
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

        if key is not None:
            self._update_listeners()

    @property
    def modifier_1(self):
        return self.modifier_1

    @modifier_1.setter
    def modifier_1(self, key):
        self._modifier_1 = key

        if key is not None:
            self._update_listeners()

    @property
    def modifier_2(self):
        return self.modifier_2

    @modifier_2.setter
    def modifier_2(self, key):
        self._modifier_2 = key

        if key is not None:
            self._update_listeners()

    def _update_listeners(self):
        modifiers = []

        if self._modifier_2:
            modifiers.append(self._modifier_2)

        if self._modifier_1:
            modifiers.append(self._modifier_1)

        sort_modifiers(modifiers)
        keys = modifiers + [self._key]

        event_name = "-".join(keys)

        # Bind keys
        self._listener.ignoreAll()
        self._listener.accept(event_name, self._on_event_down)
        self._listener.accept("buttonUp", self._on_button_up)
        self._listener.accept("buttonDown", self._on_button_down)

        # Record the keys we listen for
        self._listen_keys = keys

    def _on_event_down(self):
        self._received_event = True
        self._event_just_changed = True

    def _on_event_up(self):
        self._received_event = False
        self._event_just_changed = True

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

    @property
    def desires_positive_trigger(self):
        do_trigger = self._event_just_changed
        self._event_just_changed = False
        return do_trigger

    @property
    def desires_positive_state(self):
        return self._received_event


class MouseSensor(SCASensor):

    def __init__(self):
        pass