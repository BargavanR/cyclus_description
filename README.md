# Cyclus Description

This workspace contains the `cyclus_description` ROS 2 package for the integrated Cyclus stationary structure and EMRAC carrier system.

## Author

BARGAVAN R  
bargavanr01@gmail.com

## Setup

```bash
mkdir -p cyclus/src
cd cyclus/src
git clone <your-repository-url>
cd ..
colcon build
source install/setup.bash
```

## Run The Integrated System

Launch Gazebo with the integrated system:

```bash
ros2 launch cyclus_description cyclus_integrated.launch.py
```

## Run The Motion Sequence

In a new terminal:

```bash
cd cyclus
source install/setup.bash
ros2 run cyclus_description emrac_sequence_planner.py
```
