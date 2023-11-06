ARG ROS_DISTRO="humble"

FROM docker.io/ros:${ROS_DISTRO}

# See https://github.com/opencontainers/runc/issues/2517
RUN echo 'APT::Sandbox::User "root";' > /etc/apt/apt.conf.d/sandbox-disable

ENV ROS_OVERLAY /opt/ros/open-mcp

WORKDIR $ROS_OVERLAY

COPY open_mcp_blender src/open-mcp-blender/open_mcp_blender
COPY resource src/open-mcp-blender/resource
COPY test src/open-mcp-blender/test
COPY package.xml src/open-mcp-blender/package.xml
COPY setup.cfg src/open-mcp-blender/setup.cfg
COPY setup.py src/open-mcp-blender/setup.py

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
