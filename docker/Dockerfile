FROM ubuntu:24.04 AS base
RUN userdel -r ubuntu
SHELL ["/bin/bash", "-c"]

# ROS 2 #
ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}

# Prerequisites
RUN \
  # Install APT dependencies
  apt-get update\
  && apt-get install -y --no-install-recommends \
  build-essential \
  ca-certificates \
  cmake \
  curl \
  lcov \
  python3-pip \
  software-properties-common \
  sudo \
  wget \
  && rm -rf /var/lib/apt/lists/* \
  # Install Python dependencies
  && pip3 install --break-system-packages \
  fastcov

# Install the ROS dependencies
RUN \
  # Add the ROS 2 apt repository
  add-apt-repository universe \
  && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null \
  # Install the ROS2 packages and colcon
  && apt-get update \
  && apt-get install -y --no-install-recommends \
  colcon \
  python3-colcon-common-extensions \
  python3-colcon-clean \
  python3-colcon-cmake \
  python3-colcon-defaults \
  python3-colcon-mixin \
  ros-${ROS_DISTRO}-ament-cmake-catch2 \
  ros-${ROS_DISTRO}-catch-ros2 \
  ros-${ROS_DISTRO}-ros-base \
  ros-${ROS_DISTRO}-rqt \
  ros-${ROS_DISTRO}-rqt-gui \
  ros-${ROS_DISTRO}-rqt-common-plugins \
  ros-${ROS_DISTRO}-rviz2 \
  && rm -rf /var/lib/apt/lists/*

# Remove display warnings
RUN mkdir /tmp/runtime-root && chmod -R 0700 /tmp/runtime-root
ENV XDG_RUNTIME_DIR="/tmp/runtime-root"
ENV NO_AT_BRIDGE=1

# Set up the entrypoint
COPY ./docker/assets/entrypoint.sh /
ENTRYPOINT [ "/entrypoint.sh" ]

#####################
# Development Stage #
#####################
FROM base AS dev

# Create a dev container with a user
ARG USERNAME=dev
ARG UID=1000
ARG GID=1000

# Create new user and home directory
RUN \
  groupadd --gid ${GID} ${USERNAME} \
  && useradd --uid ${UID} --gid ${GID} --create-home ${USERNAME} \
  && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
  && chmod 0440 /etc/sudoers.d/${USERNAME} \
  && mkdir -p /home/${USERNAME} \
  && chown -R ${UID}:${GID} /home/${USERNAME} \
  # Set the ownership of the autonomy workspace to the new user
  && mkdir /project_ws \
  && chown -R ${UID}:${GID} /project_ws/ \
  # Prevent a display warning
  && chown -R ${UID}:${GID} /tmp/runtime-root

RUN \
  # Install dev tools
  apt-get update && \
  apt-get install -y --no-install-recommends \
  clang-format \
  gdb \
  git \
  less \
  linux-tools-common \
  linux-tools-generic \
  nano \
  tree && \
  rm -rf /var/lib/apt/lists/*

USER ${USERNAME}

RUN \
  echo "source /entrypoint.sh" >> /home/${USERNAME}/.bashrc
