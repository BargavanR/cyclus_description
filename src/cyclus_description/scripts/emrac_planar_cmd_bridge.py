#!/usr/bin/env python3
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class EmracPlanarCommandBridge(Node):
    def __init__(self) -> None:
        super().__init__('emrac_planar_cmd_bridge')
        self._pub = self.create_publisher(Float64MultiArray, '/emrac_planar_controller/commands', 10)
        self._sub = self.create_subscription(
            Float64MultiArray,
            '/emrac_planar_cmd',
            self._handle_cmd,
            10,
        )
        self.get_logger().info(
            'Listening on /emrac_planar_cmd and forwarding [axis_1_m, axis_2_m] to /emrac_planar_controller/commands'
        )

    def _handle_cmd(self, msg: Float64MultiArray) -> None:
        if len(msg.data) != 2:
            self.get_logger().warn('Expected 2 values: [axis_1_m, axis_2_m]')
            return

        out = Float64MultiArray()
        out.data = [float(msg.data[0]), float(msg.data[1])]
        self._pub.publish(out)


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
