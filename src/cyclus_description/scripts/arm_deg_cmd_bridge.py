#!/usr/bin/env python3
import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class ArmDegCommandBridge(Node):
    def __init__(self) -> None:
        super().__init__('arm_deg_cmd_bridge')
        self._pub = self.create_publisher(Float64MultiArray, '/arm_position_controller/commands', 10)
        self._sub = self.create_subscription(
            Float64MultiArray,
            '/emrac_arm_deg_cmd',
            self._handle_cmd,
            10,
        )
        self.get_logger().info(
            'Listening on /emrac_arm_deg_cmd, forwarding [plate_lift_m, arm1_deg, arm2_deg, arm3_deg, arm4_deg] to /arm_position_controller/commands'
        )

    def _handle_cmd(self, msg: Float64MultiArray) -> None:
        if len(msg.data) != 5:
            self.get_logger().warn(
                'Expected 5 values: [plate_lift_m, arm_joint_1_deg, arm_joint_2_deg, arm_joint_3_deg, arm_joint_4_deg]'
            )
            return

        plate_lift = float(msg.data[0])
        arm_deg = list(msg.data[1:])

        out = Float64MultiArray()
        out.data = [plate_lift] + [math.radians(value) for value in arm_deg]
        self._pub.publish(out)


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
