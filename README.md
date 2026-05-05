# Cyclus Description

This workspace contains the `cyclus_description` ROS 2 package for the Cyclus stationary frame, the EMRAC carrier assemblies, and the integrated Gazebo simulation used for motion testing.

## Author

BARGAVAN R  
bargavanr01@gmail.com

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
