import bpy


class OmcpPanel(bpy.types.Panel):
    bl_label = "omcp"
    bl_idname = "PANEL_PT_OMCP"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Motion Control"

    def draw(self, context):
        self.layout.label(icon="INFO", text="Hello, world")
        self.layout.operator("omcp.transfer")
        self.layout.operator("omcp.subscribe")
        self.layout.operator("omcp.action")

