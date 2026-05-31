# my_turtlebot

ROS 2 Python nodes for driving a TurtleBot3 with keyboard controls or simple
scripted trajectories.

## Nodes

- `teleop_key`: reads `W`, `A`, `S`, `D`, space, and `Q` from the terminal.
- `trajectory`: publishes a circle, square, or figure-eight command sequence.

Both nodes publish `geometry_msgs/msg/TwistStamped` messages to `/cmd_vel`.

## Requirements

- ROS 2 Jazzy installed and sourced
- TurtleBot3 Gazebo, if running in simulation

Install the optional simulator:

```bash
sudo apt update
sudo apt install ros-jazzy-turtlebot3-gazebo
```

## Build

From the workspace root:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --base-paths my_turtlebot
source install/setup.bash
```

## Run

Start a TurtleBot3 Gazebo world in one terminal:

```bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Run keyboard teleop from another terminal:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run my_turtlebot teleop_key
```

Run a scripted trajectory:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run my_turtlebot trajectory --ros-args -p shape:=circle
```

Supported trajectory shapes are `circle`, `square`, and `figure8`.

## Teleop Controls

| Key | Action |
| --- | --- |
| `W` | Move forward |
| `S` | Move backward |
| `A` | Turn left |
| `D` | Turn right |
| `Space` | Stop |
| `Q` | Stop and quit |

Keep the teleop terminal focused while driving.
