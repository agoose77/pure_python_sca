class SCAEventManager(object):

    def __init__(self):
        self.sensors = []
        self.actuators = []
        self.controllers = []

        self._active_actuators = set()

    def update(self):
        triggered_sensors = [s for s in self.sensors if s.evaluate()]
        triggered_controllers = set()

        active_actuators = self._active_actuators
        for sensor in triggered_sensors:
            sensor.triggered = True
            print(sensor, "TRIGGEREd")

            for controller in sensor.controllers:
                controller.on_triggered(sensor)

                # Add any triggered controllers
                for actuator in controller.actuators:
                    if not actuator.active:
                        continue

                    active_actuators.add(actuator)

            sensor.triggered = False

        to_remove = []

        # Update actuators
        for actuator in active_actuators:
            if not actuator.active:
                to_remove.append(actuator)
                continue

            actuator.on_update()

        # Newly disabled actuators
        for actuator in to_remove:
            active_actuators.remove(actuator)