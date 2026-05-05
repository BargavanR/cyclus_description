#!/usr/bin/env python3
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class EmracSequencePlanner(Node):
    def __init__(self) -> None:
        super().__init__('emrac_sequence_planner')
        self._planar_pub = self.create_publisher(Float64MultiArray, '/emrac_planar_cmd', 10)
        self._arm_pub = self.create_publisher(Float64MultiArray, '/emrac_arm_deg_cmd', 10)

    def _publish_planar(self, emrac_id: int, axis_1: float, axis_2: float) -> None:
        msg = Float64MultiArray()
        msg.data = [float(emrac_id), float(axis_1), float(axis_2)]
        self._planar_pub.publish(msg)
        self.get_logger().info(f'EMRAC {emrac_id} planar -> [{axis_1}, {axis_2}]')

    def _publish_arm(self, emrac_id: int, plate: float, a1: float, a2: float, a3: float, a4: float) -> None:
        msg = Float64MultiArray()
        msg.data = [float(emrac_id), float(plate), float(a1), float(a2), float(a3), float(a4)]
        self._arm_pub.publish(msg)
        self.get_logger().info(
            f'EMRAC {emrac_id} arm -> plate {plate}, angles [{a1}, {a2}, {a3}, {a4}]'
        )

    def _pause(self, seconds: float) -> None:
        end_time = time.time() + seconds
        while rclpy.ok() and time.time() < end_time:
            rclpy.spin_once(self, timeout_sec=0.1)

    def run_sequence(self) -> None:
        self.get_logger().info('Waiting 2 seconds for controllers/subscribers...')
        self._pause(2.0)

        self._publish_planar(1, 0.0, 0.41)
        self._pause(2.0)
        self._publish_planar(1, 1.5, 0.41)
        self._pause(2.0)
        self._publish_arm(1, 0.4, -43.0, -43.0, 43.0, -43.0)
        self._pause(3.0)
        self._publish_arm(1, 0.0, 0.0, 0.0, 0.0, 0.0)
        self._pause(2.0)
        self._publish_planar(1, -1.5, 0.41)
        self._pause(2.0)
        self._publish_planar(1, -1.5, -1.91)
        self._pause(2.0)

        self._publish_planar(2, 0.0, 0.91)
        self._pause(2.0)
        self._publish_planar(2, 1.5, 0.91)
        self._pause(2.0)
        self._publish_arm(2, 0.4, -43.0, -43.0, 43.0, -43.0)
        self._pause(3.0)
        self._publish_arm(2, 0.0, 0.0, 0.0, 0.0, 0.0)
        self._pause(2.0)
        self._publish_planar(2, -1.5, 0.91)
        self._pause(2.0)
        self._publish_planar(2, -1.5, -0.91)
        self._pause(2.0)

        self.get_logger().info('Sequence complete.')


def main() -> None:
    rclpy.init()
    node = EmracSequencePlanner()
    try:
        node.run_sequence()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
