#! /bin/bash

source /opt/ros/${ROS_DISTRO}/setup.bash

# Source the overlay workspace, if built
if [ -f /project_ws/install/local_setup.bash ]
then
  source /project_ws/install/local_setup.bash
fi

export PROJECT_WS=/project_ws

# Execute the command passed into this entrypoint
exec "$@"
