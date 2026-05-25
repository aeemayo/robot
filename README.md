# my_turtlebot

Keyboard teleoperation node for TurtleBot3 using ROS 2.

## Requirements
- ROS 2 Jazzy installed and sourced
- TurtleBot3 Gazebo (optional for simulation)

Install simulation packages (optional):

```
sudo apt update
sudo apt install ros-jazzy-turtlebot3-gazebo
```

## Build

From the workspace root:

```
source /opt/ros/jazzy/setup.bash
colcon build --base-paths my_turtlebot
source install/setup.bash
```

## Run

Start the simulation (optional):

```
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Run the teleop node:

```
source /opt/ros/jazzy/setup.bash
source /home/aeem/Downloads/robot/install/setup.bash
ros2 run my_turtlebot teleop_key
```

## Controls
- W: forward
- S: backward
- A: turn left
- D: turn right
- SPACE: stop
- Q: quit

## Notes
- The node publishes to /cmd_vel using geometry_msgs/msg/TwistStamped.
- Use a terminal with focus for key input.
