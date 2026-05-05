#!/usr/bin/env python3
import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class ArmDegCommandBridge(Node):
    def __init__(self) -> None:
        super().__init__('arm_deg_cmd_bridge')
        self._publishers = {
            1: self.create_publisher(Float64MultiArray, '/emrac_1_arm_controller/commands', 10),
            2: self.create_publisher(Float64MultiArray, '/emrac_2_arm_controller/commands', 10),
            3: self.create_publisher(Float64MultiArray, '/emrac_3_arm_controller/commands', 10),
            4: self.create_publisher(Float64MultiArray, '/emrac_4_arm_controller/commands', 10),
        }
        self._sub = self.create_subscription(
            Float64MultiArray,
            '/emrac_arm_deg_cmd',
            self._handle_cmd,
            10,
        )
        self.get_logger().info(
            'Listening on /emrac_arm_deg_cmd and forwarding [emrac_id, plate_lift_m, arm1_deg, arm2_deg, arm3_deg, arm4_deg]'
        )

    def _handle_cmd(self, msg: Float64MultiArray) -> None:
        if len(msg.data) != 6:
            self.get_logger().warn(
                'Expected 6 values: [emrac_id, plate_lift_m, arm_joint_1_deg, arm_joint_2_deg, arm_joint_3_deg, arm_joint_4_deg]'
            )
            return

        emrac_id = int(msg.data[0])
        if emrac_id not in self._publishers:
            self.get_logger().warn('EMRAC id must be 1, 2, 3, or 4')
            return

        plate_lift = float(msg.data[1])
        arm_deg = list(msg.data[2:])

        out = Float64MultiArray()
        out.data = [plate_lift] + [math.radians(value) for value in arm_deg]
        self._publishers[emrac_id].publish(out)


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
