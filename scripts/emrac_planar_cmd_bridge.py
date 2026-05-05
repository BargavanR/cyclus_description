#!/usr/bin/env python3
# File: emrac_planar_cmd_bridge.py
# Purpose: Bridge integrated EMRAC planar commands to the selected planar controller.
# Author: BARGAVAN R
# Contact: bargavanr01@gmail.com

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class EmracPlanarCommandBridge(Node):
    def __init__(self) -> None:
        super().__init__('emrac_planar_cmd_bridge')
        self._publishers = {
            1: self.create_publisher(Float64MultiArray, '/emrac_1_planar_controller/commands', 10),
            2: self.create_publisher(Float64MultiArray, '/emrac_2_planar_controller/commands', 10),
            3: self.create_publisher(Float64MultiArray, '/emrac_3_planar_controller/commands', 10),
            4: self.create_publisher(Float64MultiArray, '/emrac_4_planar_controller/commands', 10),
        }
        self.create_subscription(Float64MultiArray, '/emrac_planar_cmd', self._handle_cmd, 10)
        self.get_logger().info(
            'Listening on /emrac_planar_cmd and forwarding [emrac_id, axis_1_m, axis_2_m]'
        )

    def _handle_cmd(self, msg: Float64MultiArray) -> None:
        if len(msg.data) != 3:
            self.get_logger().warn('Expected 3 values: [emrac_id, axis_1_m, axis_2_m]')
            return

        emrac_id = int(msg.data[0])
        if emrac_id not in self._publishers:
            self.get_logger().warn('EMRAC id must be 1, 2, 3, or 4')
            return

        out = Float64MultiArray()
        out.data = [float(msg.data[1]), float(msg.data[2])]
        self._publishers[emrac_id].publish(out)


def main() -> None:
    rclpy.init()
    node = EmracPlanarCommandBridge()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
