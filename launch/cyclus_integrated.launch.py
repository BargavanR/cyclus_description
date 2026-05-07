# File: cyclus_integrated.launch.py
# Purpose: Launch the integrated Cyclus stationary and EMRAC system in Gazebo for the cyclus_description package.
# Author: BARGAVAN R
# Contact: bargavanr01@gmail.com

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('cyclus_description')
    world = PathJoinSubstitution([pkg_share, 'worlds', 'cyclus_empty.world.sdf'])
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'cyclus_integrated_system.urdf.xacro'])
    emrac_axis_1_xyz = LaunchConfiguration('emrac_axis_1_xyz')
    emrac_axis_2_xyz = LaunchConfiguration('emrac_axis_2_xyz')


    robot_description = ParameterValue(Command([
        'xacro ',
        xacro_file,
        ' emrac_axis_1_xyz:=', emrac_axis_1_xyz,
        ' emrac_axis_2_xyz:=', emrac_axis_2_xyz,

    ]), value_type=str)

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
                arguments=['-name', 'cyclus_integrated_system', '-topic', 'robot_description'],
            )
        ],
    )

    joint_state_broadcaster_spawner = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                output='screen',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
            )
        ],
    )

    spawner_specs = [
        (7.0, 'emrac_1_planar_controller'),
        (9.0, 'emrac_2_planar_controller'),
        (11.0, 'emrac_3_planar_controller'),
        (13.0, 'emrac_4_planar_controller'),
        (15.0, 'emrac_1_arm_controller'),
        (17.0, 'emrac_2_arm_controller'),
        (19.0, 'emrac_3_arm_controller'),
        (21.0, 'emrac_4_arm_controller'),
    ]
    controller_spawners = [
        TimerAction(
            period=period,
            actions=[
                Node(
                    package='controller_manager',
                    executable='spawner',
                    output='screen',
                    arguments=[controller_name, '--controller-manager', '/controller_manager'],
                )
            ],
        )
        for period, controller_name in spawner_specs
    ]

    planar_cmd_bridge = Node(
        package='cyclus_description',
        executable='emrac_planar_cmd_bridge.py',
        output='screen',
    )

    arm_deg_cmd_bridge = Node(
        package='cyclus_description',
        executable='arm_deg_cmd_bridge.py',
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument('emrac_axis_1_xyz', default_value='1,0,0'),
        DeclareLaunchArgument('emrac_axis_2_xyz', default_value='0,0,-1'),

        gz_sim,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        *controller_spawners,
        planar_cmd_bridge,
        arm_deg_cmd_bridge,
    ])
