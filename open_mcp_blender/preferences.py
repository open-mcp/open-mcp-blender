import addon_utils
import bpy
from bpy.props import IntProperty


class ReloadOpenMcpAddonOperator(bpy.types.Operator):
    bl_idname = "open_mcp.restart_and_reload_preferences"
    bl_label = "Restart open-mcp and reload the preferences"

    def execute(self, context):
        addon_utils.disable("open-mcp-blender")
        addon_utils.enable("open-mcp-blender")
        return {"FINISHED"}


class OpenMcpAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "open_mcp_blender"

    domain_id: IntProperty(
        name="ROS 2 domain ID",  # noqa: F722
        description="Safe between 0 and 101, inclusive, but possible up to 232",  # noqa: F722
        default=0,
        min=0,
        soft_max=101,
        max=232,
    )

    def draw(self, context):
        self.layout.prop(self, "domain_id")
        self.layout.operator("open_mcp.restart_and_reload_preferences")


def register():
    bpy.utils.register_class(ReloadOpenMcpAddonOperator)
    bpy.utils.register_class(OpenMcpAddonPreferences)


def unregister():
    bpy.utils.unregister_class(OmcpAddonPreferences)
    bpy.utils.unregister_class(ReloadOmcpAddonOperator)
