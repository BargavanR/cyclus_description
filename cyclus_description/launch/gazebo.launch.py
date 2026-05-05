# File: gazebo.launch.py
# Purpose: Launch the standalone stationary Cyclus scene in Gazebo for the cyclus_description package.
# Author: BARGAVAN R
# Contact: bargavanr01@gmail.com

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('cyclus_description')
    world = PathJoinSubstitution([pkg_share, 'worlds', 'cyclus_empty.world.sdf'])
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'cyclus_stationary_scene.urdf.xacro'])
    structure_gap_mm = LaunchConfiguration('structure_gap_mm')

    robot_description = Command(['xacro ', xacro_file, ' structure_gap_mm:=', structure_gap_mm])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])
        ]),
        launch_arguments={'gz_args': ['-r ', world]}.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

    spawn_entity = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                output='screen',
                arguments=['-name', 'cyclus_stationary_scene', '-topic', 'robot_description'],
            )
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('structure_gap_mm', default_value='1932.0'),
        gz_sim,
        robot_state_publisher,
        spawn_entity,
    ])
