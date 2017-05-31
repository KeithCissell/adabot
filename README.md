
[![Build Status](https://travis-ci.org/anthony-jclark/adabot.svg?branch=master)](https://travis-ci.org/anthony-jclark/adabot)

# adabot

This is a stack for the adabot robot. Below are instructions for setting up the adabot workspace; they assume that you have correctly setup your development environment. Visit [the adabot wiki](https://github.com/anthony-jclark/adabot/wiki) for more detailed instructions.

```bash
mkdir -p ~/.ros_repos/
cd ~/.ros_repos/
hub clone anthony-jclark/adabot.git
hub fork
mkdir -p ~/ros_workspaces/adabot_ws/src/
ln -s ~/.ros_repos/adabot ~/ros_workspaces/adabot_ws/src/
cd ~/ros_workspaces/adabot_ws/
catkin init
catkin config --profile debug -x _debug --cmake-args -DCMAKE_BUILD_TYPE=Debug
catkin config --profile release -x _release --cmake-args -DCMAKE_BUILD_TYPE=Release
catkin profile set debug
catkin build
```

## TODO

- split robot description into multiple files
    + primary xacro (all needed links and joints)
    + gazebo specific stuff (visualization, dynamics, sensor/actuator plugins)
    + materials xacro
    + macros xacro
- add a scaling parameter to the base xacro file
- update rviz launch file
    + option to use current urdf file
- update rviz config file
- update gazebo launch file
    + pass in world file
- add words to _gazebo package (and launch files)
- once simulation is complete start working on physical device
- check_urdf
- every needs to add themselves as authors to appropriate packages
- adabot empty world needs to use xacro file
- split-up the readme into separate files
- add script for the simple startup
- add installation of hub on linux
- add info about setting up ssh keys on github
- add general info about using git (git workflow with adabot)




