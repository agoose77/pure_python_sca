class SCAEventManager:

    def __init__(self):
        self.sensors = []
        self.actuators = []
        self.controllers = []

    def update(self):
        triggered_sensors = [s for s in self.sensors if s.evaluate()]

        triggered_controllers = []
        for sensor in triggered_sensors:
            sensor.triggered = True

            for controller in sensor.controllers:
                controller.on_triggered(sensor)

                if controller.active:
                    triggered_controllers.append(controller)

            sensor.triggered = False

        for controller in triggered_controllers:
            for actuator in controller.actuators:
                if not actuator.active:
                    continue

                actuator.on_update()