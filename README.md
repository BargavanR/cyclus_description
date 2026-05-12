# Cyclus Description

This workspace contains the `cyclus_description` ROS 2 package for the Cyclus stationary frame, the EMRAC carrier assemblies, and the integrated Gazebo simulation used for motion testing.


## Project Description

The project models a Cyclus lifting and carrier setup for battery swapping in ROS 2 Humble with Gazebo Fortress. It includes the stationary frame structure, the EMRAC carrier body, planar carriage motion for the EMRAC assemblies, and arm-plus-lift-plate actuation for test sequencing. The package is organized so the standalone stationary scene, the standalone EMRAC body, and the integrated multi-EMRAC system can all be launched from the same package.

## URDF Description

The URDF/Xacro setup is split into small reusable parts to keep the package maintainable.

The stationary frame is described as fixed geometry with left and right structures and ground rails.

The EMRAC body is described as a reusable macro so the same carrier body can be instantiated multiple times inside the integrated system.

The integrated system combines the stationary frame with multiple EMRAC instances. Each EMRAC is mounted through two prismatic carriage joints for planar motion and also includes its own lift-plate joint and four arm joints for lifting motion.

Shared materials, control macros, stationary structure macros, and integrated mounting macros are separated into include files so the top-level Xacro files stay smaller and easier to follow.

## Package Structure

`cyclus_description/urdf/` contains the main Xacro files for the standalone stationary scene, standalone EMRAC body, and integrated multi-EMRAC system.

`cyclus_description/urdf/includes/` contains shared Xacro building blocks such as materials, control declarations, stationary component macros, and integrated mounting macros.

`cyclus_description/meshes/` contains all STL assets used by the package, including the local copy of the EMRAC carrier meshes and the stationary structure meshes.

`cyclus_description/config/` contains the ROS 2 controller configuration files for both the standalone EMRAC model and the integrated multi-EMRAC system.

`cyclus_description/launch/` contains Gazebo launch files for the stationary scene, standalone EMRAC body, and integrated system.

`cyclus_description/scripts/` contains the ROS 2 helper nodes used for command bridging and for the predefined EMRAC motion sequence.

`cyclus_description/worlds/` contains the Gazebo world used for simulation.


## ROS 2 Setup

This package is intended for ROS 2 Humble on Ubuntu 22.04 with Gazebo Fortress. Start with the ROS 2 Desktop installation, then add the Gazebo and ros2_control packages used by the Cyclus simulation.

Official references:

- ROS 2 Humble Ubuntu install: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html
- ROS 2 Humble colcon tutorial: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html
- ROS/Gazebo integration package: https://docs.ros.org/en/humble/p/ros_gz/
- gz_ros2_control Humble install: https://control.ros.org/humble/doc/gz_ros2_control/doc/index.html

### 1. Install ROS 2 Humble Desktop

Follow the official ROS 2 Humble Ubuntu deb setup first: set locale, enable the Ubuntu Universe repository, add the ROS 2 apt source, then update apt.

After the ROS 2 apt source is configured, install ROS 2 Desktop and the standard ROS development tools:

```bash
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop ros-dev-tools python3-colcon-common-extensions
```

Source ROS 2 in every terminal that will build or run the package:

```bash
source /opt/ros/humble/setup.bash
```

Optional: add the source command to `~/.bashrc` so new terminals are ready automatically.

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### 2. Install Cyclus ROS/Gazebo dependencies

Install the packages required by `cyclus_description/package.xml`, the launch files, the Xacro files, and the controller YAML:

```bash
sudo apt update
sudo apt install \
  ros-humble-ros-gz \
  ros-humble-gz-ros2-control \
  ros-humble-controller-manager \
  ros-humble-joint-state-broadcaster \
  ros-humble-position-controllers \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-rclpy \
  ros-humble-std-msgs \
  ros-humble-launch \
  ros-humble-launch-ros
```

What these provide:

- `ros-humble-desktop`: ROS 2 Humble desktop tools, RViz, demos, and common runtime packages.
- `ros-dev-tools` and `python3-colcon-common-extensions`: build and workspace tools for `colcon build`.
- `ros-humble-ros-gz`: ROS 2 integration packages for Gazebo, including `ros_gz_sim`, which this package uses to launch Gazebo.
- `ros-humble-gz-ros2-control`: Gazebo Sim plugin for `ros2_control`; required by `libgz_ros2_control-system.so` and `gz_ros2_control/GazeboSimSystem` in the URDF/Xacro files.
- `ros-humble-controller-manager`: provides the `spawner` executable used by the launch files.
- `ros-humble-joint-state-broadcaster` and `ros-humble-position-controllers`: provide the controller types used in `config/*.yaml`.
- `ros-humble-robot-state-publisher` and `ros-humble-xacro`: publish and generate the robot description from Xacro.
- `ros-humble-rclpy` and `ros-humble-std-msgs`: required by the Python helper nodes in `scripts/`.
- `ros-humble-launch` and `ros-humble-launch-ros`: required by the Python launch files.

## Running Setup

Create the workspace and clone the repository into the `src` folder.

```bash
mkdir -p cyclus/src
cd cyclus/src
git clone <your-repository-url>
```

Move to the workspace root, build the workspace, and source the setup file.

```bash
cd ..
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

Launch the integrated Gazebo simulation.

```bash
ros2 launch cyclus_description cyclus_integrated.launch.py
```

In a new terminal, source the workspace again and run the motion-sequence node.

```bash
cd cyclus
source install/setup.bash
ros2 run cyclus_description emrac_sequence_planner.py
```
