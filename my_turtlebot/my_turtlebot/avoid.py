"""Obstacle avoidance node for TurtleBot3.

Subscribes to /scan (LaserScan) and publishes TwistStamped to /cmd_vel.
Drives forward until an obstacle is detected within THRESHOLD metres in the
front ~30° arc, then turns left until the path is clear.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped

THRESHOLD = 0.5   # metres
SPEED = 0.2       # m/s forward
TURN = 0.5        # rad/s turning


class AvoidNode(Node):
    """Reactive obstacle-avoidance controller."""

    def __init__(self) -> None:
        super().__init__("avoid")
        self.publisher = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.subscription = self.create_subscription(
            LaserScan, "/scan", self.scan_cb, 10
        )
        self.timer = self.create_timer(0.1, self.drive)
        self.blocked: bool = False

    # ------------------------------------------------------------------ #
    #  Callbacks                                                          #
    # ------------------------------------------------------------------ #

    def scan_cb(self, msg: LaserScan) -> None:
        """Analyse the front ~30° arc for obstacles."""
        n = len(msg.ranges)
        window = n // 12                       # ≈30° total (15° each side)
        front = list(msg.ranges[:window]) + list(msg.ranges[-window:])

        valid = [r for r in front if msg.range_min < r < msg.range_max]
        self.blocked = any(r < THRESHOLD for r in valid)

    def drive(self) -> None:
        """Publish velocity commands on a 10 Hz timer."""
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = "base_link"

        if self.blocked:
            cmd.twist.linear.x = 0.0
            cmd.twist.angular.z = TURN
            self.get_logger().info("Obstacle! Turning...")
        else:
            cmd.twist.linear.x = SPEED
            cmd.twist.angular.z = 0.0

        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(AvoidNode())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
