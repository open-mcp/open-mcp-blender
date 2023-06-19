ARG ROS_DISTRO="humble"

FROM docker.io/ros:${ROS_DISTRO}

# See https://github.com/opencontainers/runc/issues/2517
RUN echo 'APT::Sandbox::User "root";' > /etc/apt/apt.conf.d/sandbox-disable

ENV ROS_OVERLAY /opt/ros/omcp

WORKDIR $ROS_OVERLAY

# Workaround for https://github.com/emanuelbuholzer/omcp_blender/issues/1
RUN apt-get update &&  \
    apt-get install -y python3-pip &&  \
    python3 -m pip install pytest-blender && \
    rm -rf /var/lib/apt/lists/

COPY addons src/omcp_blender/addons
COPY resource src/omcp_blender/resource
COPY test src/omcp_blender/test
COPY package.xml src/omcp_blender/package.xml
COPY pytest.ini src/omcp_blender/pytest.ini
COPY setup.cfg src/omcp_blender/setup.cfg
COPY setup.py src/omcp_blender/setup.py

RUN apt-get update && \
    rosdep install -iy --from-paths src && \
    rm -rf /var/lib/apt/lists/

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon build --continue-on-error

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && \
    colcon test ; \
    colcon test-result --verbose

RUN sed --in-place --expression \
    '$isource "${ROS_OVERLAY}/install/setup.bash"' \
    /ros_entrypoint.sh
