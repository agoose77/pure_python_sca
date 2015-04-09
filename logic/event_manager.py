class SCAEventManager:

    def __init__(self):
        self.sensors = []
        self.actuators = []
        self.controllers = []

    def update(self):
        triggered_sensors = [s for s in self.sensors if s.evaluate()]

        triggered_controllers = set()
        for sensor in triggered_sensors:
            sensor.triggered = True

            for controller in sensor.controllers:
                controller.on_triggered(sensor)

                triggered_controllers.add(controller)

            sensor.triggered = False

        for controller in triggered_controllers:
            for actuator in controller.actuators:
                if not actuator.active:
                    continue

                actuator.on_update()