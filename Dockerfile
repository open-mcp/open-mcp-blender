ARG ROS_DISTRO="humble"

FROM docker.io/ros:${ROS_DISTRO}

# See https://github.com/opencontainers/runc/issues/2517
RUN echo 'APT::Sandbox::User "root";' > /etc/apt/apt.conf.d/sandbox-disable

ENV ROS_OVERLAY /opt/ros/omcp

WORKDIR $ROS_OVERLAY

COPY omcp_blender src/omcp_blender/omcp_blender
COPY resource src/omcp_blender/resource
COPY test src/omcp_blender/test
COPY package.xml src/omcp_blender/package.xml
COPY setup.cfg src/omcp_blender/setup.cfg
COPY setup.py src/omcp_blender/setup.py

RUN git clone https://github.com/emanuelbuholzer/ros2_blender.git src/ros2_blender

RUN apt-get update && \
    rosdep install -iy --from-paths src && \
    rm -rf /var/lib/apt/lists/

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon build --symlink-install --continue-on-error

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon test ; \
    colcon test-result --verbose

RUN sed --in-place --expression \
    '$isource "${ROS_OVERLAY}/install/setup.bash"' \
    /ros_entrypoint.sh
