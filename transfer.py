import bpy

from .rig import apply_q, ARMATURE_GHOST, ARMATURE_MODEL


class TransferOperator(bpy.types.Operator):
    bl_idname = "omcp.transfer"
    bl_label = "Transfer joint positions"

    armature: bpy.props.EnumProperty(
        items=[
            (ARMATURE_GHOST, "Physical robot", "Armature of the physical robot", 0),
            (ARMATURE_MODEL, "Rigged robot", "Armature of the rigged robot model", 1),
        ],
        name="Armature",
        description="Armature of an omcp robot",
        default="Armature"
    )

    # TODO: set soft and hard limits
    joint_positions: bpy.props.FloatVectorProperty(
        name="Joint positions",
        description="Joint positions in rad from base to the end effector",
        default=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        size=6
    )

    def execute(self, context):
        apply_q(self.armature, self.joint_positions)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)



