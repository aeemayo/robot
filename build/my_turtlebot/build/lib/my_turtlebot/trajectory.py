"""Trajectory tracking node for TurtleBot3."""

import math
import time

import rclpy
from geometry_msgs.msg import Twist, TwistStamped
from rclpy.node import Node
from std_msgs.msg import Header

LINEAR_SPEED = 0.2
PUBLISH_HZ = 20.0


class TrajectoryNode(Node):
    """ROS 2 node that publishes simple trajectories."""

    def __init__(self) -> None:
        super().__init__("trajectory_node")
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.declare_parameter("shape", "circle")

    def publish(
        self, linear: float = 0.0, angular: float = 0.0, duration: float = 1.0
    ) -> None:
        """Publish Twist commands at 50 Hz for a duration in seconds."""
        msg = TwistStamped()
        msg.header.frame_id = "base_link"
        msg.twist.linear.x = linear
        msg.twist.angular.z = angular
        end_time = time.time() + duration
        while time.time() < end_time and rclpy.ok():
            msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.02)

    def circle(self, radius: float = 0.5) -> None:
        """Drive one full circle."""
        angular = LINEAR_SPEED / radius
        duration = (2.0 * math.pi * radius) / LINEAR_SPEED
        self.publish(LINEAR_SPEED, angular, duration)

    def square(self, side: float = 1.0) -> None:
        """Drive a square path."""
        speed = 0.2
        for _ in range(4):
            self.publish(speed, 0.0, side / speed)
            self.publish(0.0, 0.0, 0.3)
            self.publish(0.0, math.pi / 2, 2.0)
            self.publish(0.0, 0.0, 0.3)

    def figure8(self, radius: float = 0.5) -> None:
        """Drive a figure-eight path."""
        angular = LINEAR_SPEED / radius
        duration = (2.0 * math.pi * radius) / LINEAR_SPEED
        self.publish(LINEAR_SPEED, -angular, duration)
        self.publish(LINEAR_SPEED, angular, duration)

    def run(self) -> None:
        """Run the trajectory selected by the shape parameter."""
        shape = self.get_parameter("shape").value
        if shape == "circle":
            self.circle()
        elif shape == "square":
            self.square()
        elif shape == "figure8":
            self.figure8()
        else:
            self.get_logger().warn(
                "Unknown shape '%s'; defaulting to circle.", shape
            )
            self.circle()
        self.pub.publish(TwistStamped())


def main(args=None) -> None:
    """Entry point for trajectory node."""
    rclpy.init(args=args)
    node = TrajectoryNode()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
