from json import loads
from python_importer import SCALogicImporter

converted = '''{"controllers": [{"states": 1, "type": "PYTHON", "mode": "MODULE", "name": "Python", "use_debug": false, "show_expanded": true, "use_priority": false, "actuators": [], "active": true, "module": "test_module.main"}], "actuators": [], "sensors": [{"invert": true, "type": "ALWAYS", "controllers": ["Python"], "name": "Always1", "frequency": 0, "use_tap": false, "use_pulse_true_level": false, "use_pulse_false_level": false, "active": true, "pin": false, "show_expanded": true, "use_level": false}]}'''
data = loads(converted)

importer = SCALogicImporter(data)

event_manager = importer.event_manager

print("Expect a single print statement, False positive state")
event_manager.update()
event_manager.update()
event_manager.update()
