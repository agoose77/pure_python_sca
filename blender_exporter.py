from inspect import getmembers


def is_primitive(value):
    return isinstance(value, (int, bool, str, float))


def get_primitive_attributes_as_dict(obj):
    as_dict = {}
    
    for name, value in getmembers(obj):
        if name.startswith("_"):
            continue
        
        if not is_primitive(value):
            continue
        
        as_dict[name] = value
    
    return as_dict


def sca_to_dict(obj):
    as_dict = get_primitive_attributes_as_dict(obj)        
    
    if hasattr(obj, "controllers"):
        as_dict['controllers'] = [c.name for c in obj.controllers]
    
    if hasattr(obj, "sensors"):
        as_dict['sensors'] = [c.name for c in obj.controllers]
    
    if hasattr(obj, "actuators"):
        as_dict['actuators'] = [c.name for c in obj.actuators]
    
    return as_dict


def dump_logic_bricks(obj):
    game = obj.game
    
    sensor_data = []
    for sensor in game.sensors:
        as_dict = sca_to_dict(sensor)
        sensor_data.append(as_dict)
    
    controller_data = []
    for controller in game.controllers:
        as_dict = sca_to_dict(controller)
        controller_data.append(as_dict)
    
    actuator_data = []
    for actuator in game.actuators:
        as_dict = sca_to_dict(actuator)
        actuator_data.append(as_dict)

    return dict(sensors=sensor_data, controllers=controller_data, actuators=actuator_data)        

