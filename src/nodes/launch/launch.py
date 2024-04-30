from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='nodes',
            executable='nodeOne',
            name='nodeOne',
        ),
        Node(
            package='nodes',
            executable='nodeTwo',
            name='nodeTwo',
            arguments=['6', '3']
        )
    ])
