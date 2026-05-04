cmake_minimum_required(VERSION 3.8)
project(cyclus_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch meshes urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/arm_deg_cmd_bridge.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
