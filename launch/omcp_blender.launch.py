import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackagePrefix


def generate_launch_description():
    declared_arguments = []

    ros2_blender_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("ros2_blender"), "launch"),
                "/blender.launch.py",
            ]
        ),
        launch_arguments={
            "addons": "omcp_blender",
            "addon_paths": [
                PathJoinSubstitution(
                    [
                        FindPackagePrefix("omcp_blender"),
                        "lib",
                        "python3.10",
                        "site-packages",
                        "omcp_blender",
                    ]
                )
            ],
        }.items(),
    )
    declared_arguments.append(ros2_blender_launch)

    return LaunchDescription(declared_arguments)
