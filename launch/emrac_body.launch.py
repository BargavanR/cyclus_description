# File: emrac_body.launch.py
# Purpose: Launch the standalone EMRAC body model in Gazebo for the cyclus_description package.
# Author: BARGAVAN R
# Contact: bargavanr01@gmail.com

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('cyclus_description')
    world = PathJoinSubstitution([pkg_share, 'worlds', 'cyclus_showcase.world.sdf'])
    gui_config = PathJoinSubstitution([pkg_share, 'config', 'gui.config'])
    bridge_config = PathJoinSubstitution([pkg_share, 'config', 'bridge.yaml'])
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'emrac_body.urdf.xacro'])

    robot_description = Command(['xacro ', xacro_file])

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])
        ]),
        launch_arguments={'gz_args': ['-r ', world, ' --gui-config ', gui_config]}.items(),
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
                arguments=['-name', 'emrac_body', '-topic', 'robot_description'],
            )
        ],
    )

    spawner_timeout_args = [
        '--controller-manager',
        '/controller_manager',
        '--controller-manager-timeout',
        '120',
        '--service-call-timeout',
        '120',
        '--switch-timeout',
        '120',
    ]

    joint_state_broadcaster_spawner = TimerAction(
        period=4.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                output='screen',
                arguments=['joint_state_broadcaster', *spawner_timeout_args],
            )
        ],
    )

    arm_position_controller_spawner = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                output='screen',
                arguments=['arm_position_controller', *spawner_timeout_args],
            )
        ],
    )

    arm_deg_cmd_bridge = Node(
        package='cyclus_description',
        executable='arm_deg_cmd_bridge.py',
        output='screen',
    )

    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '--ros-args',
            '-p',
            ['config_file:=', bridge_config],
        ],
    )

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        ros_gz_bridge,
        joint_state_broadcaster_spawner,
        arm_position_controller_spawner,
        arm_deg_cmd_bridge,
    ])
