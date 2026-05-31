# my_turtlebot

A ROS 2 Python package for controlling a TurtleBot3 from the keyboard or by
publishing simple motion trajectories.

## What is included

- `teleop_key`: keyboard teleoperation for manual driving.
- `trajectory`: scripted circle, square, or figure-eight paths.
- Both nodes publish velocity commands on `/cmd_vel` as
  `geometry_msgs/msg/TwistStamped`.

## Requirements

- Ubuntu with ROS 2 Jazzy installed
- `colcon`
- TurtleBot3 Gazebo packages, if you want to run the nodes in simulation

Install the optional simulation packages:

```bash
sudo apt update
sudo apt install ros-jazzy-turtlebot3-gazebo
```

## Workspace Layout

```text
.
|-- README.md
`-- my_turtlebot
    |-- my_turtlebot
    |   |-- teleop_key.py
    |   `-- trajectory.py
    |-- package.xml
    `-- setup.py
```

## Build

From the workspace root:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --base-paths my_turtlebot
source install/setup.bash
```

After changing Python entry points or package metadata, rebuild and source the
workspace again.

## Run in Simulation

In one terminal, start TurtleBot3 Gazebo:

```bash
source /opt/ros/jazzy/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

In another terminal, source the workspace and run a node.

### Keyboard Teleop

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run my_turtlebot teleop_key
```

Controls:

| Key | Action |
| --- | --- |
| `W` | Move forward |
| `S` | Move backward |
| `A` | Turn left |
| `D` | Turn right |
| `Space` | Stop |
| `Q` | Stop and quit |

Keep the terminal focused while using keyboard teleop.

### Scripted Trajectories

Run the default circle trajectory:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run my_turtlebot trajectory
```

Choose a path with the `shape` parameter:

```bash
ros2 run my_turtlebot trajectory --ros-args -p shape:=circle
ros2 run my_turtlebot trajectory --ros-args -p shape:=square
ros2 run my_turtlebot trajectory --ros-args -p shape:=figure8
```

Unknown shapes fall back to `circle`.

## Troubleshooting

- If `ros2 run` cannot find `my_turtlebot`, rebuild the workspace and run
  `source install/setup.bash` from the workspace root.
- If the robot does not move in Gazebo, confirm that the simulation is running
  and that a node is publishing to `/cmd_vel`.
- If keyboard input seems ignored, click or focus the teleop terminal.
