"""Keyboard teleop node for TurtleBot3."""

import select
import sys
import termios
import time
import tty

import rclpy
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node
from std_msgs.msg import Header

LINEAR_SPEED = 0.2
ANGULAR_SPEED = 0.5


class TeleopKey(Node):
    """ROS 2 node for keyboard teleoperation."""

    def __init__(self) -> None:
        super().__init__("teleop_key")
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.linear = 0.0
        self.angular = 0.0
        self.create_timer(0.1, self._on_timer)

    def _get_key(self) -> str:
        ready, _, _ = select.select([sys.stdin], [], [], 0)
        if ready:
            return sys.stdin.read(1)
        return ""

    def _publish_twist(self, linear: float, angular: float) -> None:
        msg = TwistStamped()
        msg.header.frame_id = "base_link"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = linear
        msg.twist.angular.z = angular
        self.pub.publish(msg)

    def _handle_key(self, key: str) -> None:
        key_upper = key.upper()
        if key_upper == "W":
            self.linear = LINEAR_SPEED
            self.angular = 0.0
        elif key_upper == "S":
            self.linear = -LINEAR_SPEED
            self.angular = 0.0
        elif key_upper == "A":
            self.linear = 0.0
            self.angular = ANGULAR_SPEED
        elif key_upper == "D":
            self.linear = 0.0
            self.angular = -ANGULAR_SPEED
        elif key == " ":
            self.linear = 0.0
            self.angular = 0.0
        elif key_upper == "Q":
            self._publish_twist(0.0, 0.0)
            rclpy.shutdown()

    def _on_timer(self) -> None:
        key = self._get_key()
        if key:
            self._handle_key(key)
        self._publish_twist(self.linear, self.angular)


def main(args=None) -> None:
    """Entry point for teleop_key."""
    rclpy.init(args=args)
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    node = TeleopKey()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node._publish_twist(0.0, 0.0)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
