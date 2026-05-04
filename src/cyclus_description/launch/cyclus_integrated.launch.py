from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('cyclus_description')
    world = PathJoinSubstitution([pkg_share, 'worlds', 'cyclus_empty.world.sdf'])
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'cyclus_integrated_system.urdf.xacro'])

    structure_gap_mm = LaunchConfiguration('structure_gap_mm')
    emrac_axis_1_xyz = LaunchConfiguration('emrac_axis_1_xyz')
    emrac_axis_2_xyz = LaunchConfiguration('emrac_axis_2_xyz')
    emrac_axis_1_limit_m = LaunchConfiguration('emrac_axis_1_limit_m')
    emrac_axis_2_limit_m = LaunchConfiguration('emrac_axis_2_limit_m')
    robot_description = Command([
        'xacro ',
        xacro_file,
        ' structure_gap_mm:=', structure_gap_mm,
        ' emrac_axis_1_xyz:=', emrac_axis_1_xyz,
        ' emrac_axis_2_xyz:=', emrac_axis_2_xyz,
        ' emrac_axis_1_limit_m:=', emrac_axis_1_limit_m,
        ' emrac_axis_2_limit_m:=', emrac_axis_2_limit_m,
    ])

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
        period=4.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                output='screen',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
            )
        ],
    )

    planar_controller_spawner = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                output='screen',
                arguments=['emrac_planar_controller', '--controller-manager', '/controller_manager'],
            )
        ],
    )

    arm_controller_spawner = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                output='screen',
                arguments=['arm_position_controller', '--controller-manager', '/controller_manager'],
            )
        ],
    )

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
        DeclareLaunchArgument('structure_gap_mm', default_value='1932.0'),
        DeclareLaunchArgument('emrac_axis_1_xyz', default_value='1,0,0'),
        DeclareLaunchArgument('emrac_axis_2_xyz', default_value='0,0,-1'),
        DeclareLaunchArgument('emrac_axis_1_limit_m', default_value='0.6'),
        DeclareLaunchArgument('emrac_axis_2_limit_m', default_value='0.6'),
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        planar_controller_spawner,
        arm_controller_spawner,
        planar_cmd_bridge,
        arm_deg_cmd_bridge,
    ])
