import addon_utils
import bpy
from bpy.props import IntProperty


class ReloadOmcpAddonOperator(bpy.types.Operator):
    bl_idname = "omcp.restart_and_reload_preferences"
    bl_label = "Restart omcp and reload the preferences"

    def execute(self, context):
        addon_utils.disable("omcp_blender")
        addon_utils.enable("omcp_blender")
        return {"FINISHED"}


class OmcpAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "omcp_blender"

    domain_id: IntProperty(
        name="ROS 22 domain ID",  # noqa: F722
        description="Safe between 0 and 101, inclusive, but possible up to 232",  # noqa: F722
        default=0,
        min=0,
        soft_max=101,
        max=232,
    )

    def draw(self, context):
        self.layout.prop(self, "domain_id")
        self.layout.operator("omcp.restart_and_reload_preferences")


def register():
    bpy.utils.register_class(ReloadOmcpAddonOperator)
    bpy.utils.register_class(OmcpAddonPreferences)


def unregister():
    bpy.utils.unregister_class(OmcpAddonPreferences)
    bpy.utils.unregister_class(ReloadOmcpAddonOperator)
