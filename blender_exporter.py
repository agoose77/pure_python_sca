import bpy
from inspect import getmembers
from json import dumps
from mathutils import Vector, Euler


def is_primitive(value):
    return isinstance(value, (int, bool, str, float, tuple))


def get_primitive_attributes_as_dict(obj):
    as_dict = {}
    
    for name, value in getmembers(obj):
        if name.startswith("_"):
            continue
        
        if isinstance(value, (Vector, Euler)):
            value = tuple(value)
        
        if not is_primitive(value):
            continue
        
        as_dict[name] = value
    
    return as_dict


def sca_to_dict(obj):
    as_dict = get_primitive_attributes_as_dict(obj)        
    if obj.type == "MOTION":
        print(as_dict)
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


class LOGIC_OT_ExportLogicBricks(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.export_logic_bricks"
    bl_label = "Export Logic Bricks To Text File"""

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        converted = dump_logic_bricks(obj)
        
        try:
            text = bpy.data.texts[obj.name]
        except KeyError:
            text = bpy.data.texts.new(obj.name)
        
        text.from_string(dumps(converted))
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LOGIC_OT_ExportLogicBricks)


def unregister():
    bpy.utils.unregister_class(LOGIC_OT_ExportLogicBricks)


if __name__ == "__main__":
    register()
