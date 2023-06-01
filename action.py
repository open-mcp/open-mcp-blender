import bpy
import rclpy
import rclpy.action
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class TransferOperator(bpy.types.Operator):
    bl_idname = "omcp.action"
    bl_label = "Transfer joint positions"

    # TODO: set soft and hard limits
    joint_positions: bpy.props.FloatVectorProperty(
        name="Joint positions",
        description="Joint positions in rad from base to the end effector",
        default=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        size=6
    )

    def execute(self, context):
        node = rclpy.create_node("omcp_action")

        action_client = rclpy.action.ActionClient(
            node,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )

        if not action_client.wait_for_server(timeout_sec=5.0):
            node.get_logger().info("Action server not available")
            return {"CANCELLED"}

        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
        goal_point = JointTrajectoryPoint()
        goal_point.positions = self.joint_positions
        goal_point.time_from_start = Duration(sec=5)
        goal.trajectory.points.append(goal_point)





        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)



