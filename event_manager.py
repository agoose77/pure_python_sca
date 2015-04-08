class SCAEventManager:

    def __init__(self):
        self.sensors = []
        self.actuators = []
        self.controllers = []

    def update(self):
        triggered_sensors = []
        for sensor in self.sensors:
            was_positive = sensor.positive
            sensor.evaluate()

            if sensor.positive and (sensor.use_positive_pulse or not was_positive):
                triggered_sensors.append(sensor)

            elif sensor.use_negative_pulse or was_positive:
                triggered_sensors.append(sensor)

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