import bpy
from bpy.props import IntProperty


class OmcpAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "omcp"

    domain_id: IntProperty(
        name="ROS 22 domain ID",
        description="Safe between 0 and 101, inclusive, but possible up to 232",
        default=0,
        min=0,
        soft_max=101,
        max=232
    )

    def draw(self, context):
        self.layout.prop(self, "domain_id")


def register():
    bpy.utils.register_class(OmcpAddonPreferences)


def unregister():
    bpy.utils.unregister_class(OmcpAddonPreferences)