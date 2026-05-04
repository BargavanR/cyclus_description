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

    
    emrac_axis_1_xyz = LaunchConfiguration('emrac_axis_1_xyz')
    emrac_axis_2_xyz = LaunchConfiguration('emrac_axis_2_xyz')

    robot_description = Command([
        'xacro ',
        xacro_file,

        ' emrac_axis_1_xyz:=', emrac_axis_1_xyz,
        ' emrac_axis_2_xyz:=', emrac_axis_2_xyz,
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

    emrac_1_controller_spawner = TimerAction(
        period=7.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_1_planar_controller', '--controller-manager', '/controller_manager'])],
    )
    emrac_2_controller_spawner = TimerAction(
        period=9.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_2_planar_controller', '--controller-manager', '/controller_manager'])],
    )
    emrac_3_controller_spawner = TimerAction(
        period=11.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_3_planar_controller', '--controller-manager', '/controller_manager'])],
    )
    emrac_4_controller_spawner = TimerAction(
        period=13.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_4_planar_controller', '--controller-manager', '/controller_manager'])],
    )

    emrac_1_arm_controller_spawner = TimerAction(
        period=15.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_1_arm_controller', '--controller-manager', '/controller_manager'])],
    )
    emrac_2_arm_controller_spawner = TimerAction(
        period=17.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_2_arm_controller', '--controller-manager', '/controller_manager'])],
    )
    emrac_3_arm_controller_spawner = TimerAction(
        period=19.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_3_arm_controller', '--controller-manager', '/controller_manager'])],
    )
    emrac_4_arm_controller_spawner = TimerAction(
        period=21.0,
        actions=[Node(package='controller_manager', executable='spawner', output='screen', arguments=['emrac_4_arm_controller', '--controller-manager', '/controller_manager'])],
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
      
        DeclareLaunchArgument('emrac_axis_1_xyz', default_value='1,0,0'),
        DeclareLaunchArgument('emrac_axis_2_xyz', default_value='0,0,-1'),
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        emrac_1_controller_spawner,
        emrac_2_controller_spawner,
        emrac_3_controller_spawner,
        emrac_4_controller_spawner,
        emrac_1_arm_controller_spawner,
        emrac_2_arm_controller_spawner,
        emrac_3_arm_controller_spawner,
        emrac_4_arm_controller_spawner,
        planar_cmd_bridge,
        arm_deg_cmd_bridge,
    ])
