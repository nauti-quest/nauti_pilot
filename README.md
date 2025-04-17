# Nauti Pilot
This package contains hardcoded scripts and scripts to convert command velocity to MAVLink messages for ArduSub.

## Dependencies
* ROS Noetic
* Python 3.x
* mavros (`sudo apt-get install ros-noetic-mavros`)
* tf2 (`sudo apt-get install ros-noetic-tf2`)
* geometry_msgs
* mavros_msgs

### Python Dependencies
```bash
pip3 install numpy
```

## Build
```bash
cd <parent_directory>/<workspace>
catkin build
source devel/setup.bash
```

## How to run
1. Command Velocity to MAVLink converter: To run the command velocity to MAVLink converter, run the following command:
```bash
cd <parent_directory>/<workspace>/src/nauti_pilot/src/
python3 pilot.py
```
2. Hardcoded Scripts: To run the hardcoded scripts, call the hardcoded maneuver function inside the main function in hardcoded-scripts.py. Then run the script:
```bash
cd <parent_directory>/<workspace>/src/nauti_pilot/src/
python3 hardcoded-scripts.py
```

## Support
For issues and questions, please open an issue in this repository.
