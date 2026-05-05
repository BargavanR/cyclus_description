#!/usr/bin/env python3
# File: arm_deg_cmd_bridge.py
# Purpose: Bridge degree-based arm commands to the appropriate EMRAC position controllers.
# Author: BARGAVAN R
# Contact: bargavanr01@gmail.com

import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class ArmDegCommandBridge(Node):
    def __init__(self) -> None:
        super().__init__('arm_deg_cmd_bridge')
        self._standalone_pub = self.create_publisher(Float64MultiArray, '/arm_position_controller/commands', 10)
        self._integrated_publishers = {
            1: self.create_publisher(Float64MultiArray, '/emrac_1_arm_controller/commands', 10),
            2: self.create_publisher(Float64MultiArray, '/emrac_2_arm_controller/commands', 10),
            3: self.create_publisher(Float64MultiArray, '/emrac_3_arm_controller/commands', 10),
            4: self.create_publisher(Float64MultiArray, '/emrac_4_arm_controller/commands', 10),
        }
        self.create_subscription(Float64MultiArray, '/emrac_arm_deg_cmd', self._handle_cmd, 10)
        self.get_logger().info(
            'Listening on /emrac_arm_deg_cmd for either [plate, a1, a2, a3, a4] or [id, plate, a1, a2, a3, a4]'
        )

    def _publish_arm_command(self, publisher, plate_lift: float, arm_deg: list[float]) -> None:
        out = Float64MultiArray()
        out.data = [plate_lift] + [math.radians(value) for value in arm_deg]
        publisher.publish(out)

    def _handle_cmd(self, msg: Float64MultiArray) -> None:
        if len(msg.data) == 5:
            self._publish_arm_command(self._standalone_pub, float(msg.data[0]), list(msg.data[1:]))
            return

        if len(msg.data) == 6:
            emrac_id = int(msg.data[0])
            if emrac_id not in self._integrated_publishers:
                self.get_logger().warn('EMRAC id must be 1, 2, 3, or 4')
                return
            self._publish_arm_command(self._integrated_publishers[emrac_id], float(msg.data[1]), list(msg.data[2:]))
            return

        self.get_logger().warn(
            'Expected [plate, a1, a2, a3, a4] or [emrac_id, plate, a1, a2, a3, a4]'
        )


def main() -> None:
    rclpy.init()
    node = ArmDegCommandBridge()
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
