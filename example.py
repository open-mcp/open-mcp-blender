import rclpy
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint



def feedback_callback(feedback_msg):
    feedback = feedback_msg.feedback
    print('Received feedback: {0}'.format(feedback.actual.positions))

def main():
    rclpy.init()
    node = rclpy.create_node('follow_joint_trajectory_client')

    # Create an action client
    action_client = ActionClient(node, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')

    # Wait for the action server to become available
    if not action_client.wait_for_server(timeout_sec=5.0):
        node.get_logger().info('Action server not available')
        return

    # Create a goal message
    goal_msg = FollowJointTrajectory.Goal()

    # Set the desired joint names and positions in the goal message
    goal_msg.trajectory.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
    point1 = JointTrajectoryPoint()
    point1.positions = [1.6, 0.5, 0.5, 2.5, 0.5, 0.5]
    point1.time_from_start = Duration(sec=30)
    goal_msg.trajectory.points.append(point1)

    # Send the goal to the action server
    send_goal_future = action_client.send_goal_async(goal_msg, feedback_callback=feedback_callback)

    # Wait for the goal to complete
    rclpy.spin_until_future_complete(node, send_goal_future)
    goal_handle = send_goal_future.result()

    if not goal_handle.accepted:
        node.get_logger().info('Goal rejected by server')
        return

    # Wait for the result
    get_result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, get_result_future)
    result = get_result_future.result()
    if result.result:
        print(result.result)
        node.get_logger().info('Goal succeeded!')
    else:
        node.get_logger().info('Goal failed!')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
