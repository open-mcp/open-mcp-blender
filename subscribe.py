import bpy

import threading
import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState


from .rig import apply_q, ARMATURE_GHOST, ARMATURE_MODEL


class SubscribeOperator(bpy.types.Operator):
    bl_idname = "omcp.subscribe"
    bl_label = "Subscribe to joint positions"

    armature: bpy.props.EnumProperty(
        items=[
            (ARMATURE_GHOST, "Physical robot", "Armature of the physical robot", 0),
            (ARMATURE_MODEL, "Rigged robot", "Armature of the rigged robot model", 1),
        ],
        name="Armature",
        description="Armature of an omcp robot",
        default="Armature"
    )

    _timer = None
    _node = None
    _last_pos = None

    def execute(self, context):
        self._node = rclpy.create_node('omcp_blender_subscribe')

        self._timer = context.window_manager.event_timer_add(
            0.1, window=context.window
        )
        context.window_manager.modal_handler_add(self)

        self._node.create_subscription(
            JointTrajectoryControllerState,
            '/joint_trajectory_controller/state',
            self.listener_callback,
            10
        )
        return {"RUNNING_MODAL"}

    def __del__(self):
        try:
            if self._node:
                self._node.destroy_node()
        except ReferenceError as refer:
            print(refer)
            pass

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self._node.destroy_node()
        self._node = None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def listener_callback(self, msg: JointTrajectoryControllerState):
        self._last_pos = msg.actual.positions

    def modal(self, context, event):
        if event.type.startswith("TIMER"):
            try:
                rclpy.spin_once(self._node, timeout_sec=0)
                if self._last_pos:
                    bpy.ops.omcp.transfer("EXEC_DEFAULT", armature=self.armature, joint_positions=self._last_pos)
            except Exception as err:
                self.cancel(context)
                raise err
        return {"PASS_THROUGH"}



