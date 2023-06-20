import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    declared_arguments = []

    ros2_blender_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros2_blender'), 'launch'),
            '/blender.launch.py'])
    )
    declared_arguments.append(ros2_blender_launch)

    return LaunchDescription(declared_arguments)
