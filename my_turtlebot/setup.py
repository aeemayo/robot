"""Setuptools package configuration for my_turtlebot."""

from setuptools import setup

package_name = "my_turtlebot"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[("share/" + package_name, ["package.xml"])],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Your Name",
    maintainer_email="you@example.com",
    description="TurtleBot3 keyboard teleoperation.",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "teleop_key = my_turtlebot.teleop_key:main",
            "trajectory = my_turtlebot.trajectory:main",
        ],
    },
)
