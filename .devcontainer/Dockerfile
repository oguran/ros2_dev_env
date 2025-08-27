FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Asia/Tokyo
ARG USERNAME=dev
ARG UID=1000
ARG GID=1000

# 基本ツール・ロケール・X11/GL
RUN apt-get update && apt-get install -y \
    tzdata locales \
    build-essential cmake git curl sudo \
    gdb-multiarch \
    libusb-1.0-0-dev libudev-dev libhidapi-dev \
    net-tools iproute2 iputils-ping \
    vim unzip usbutils \
    software-properties-common \
    x11-apps xvfb mesa-utils \
    libgl1 libgl1-mesa-dev libglu1-mesa-dev libosmesa6-dev \
    libxext6 libxrender1 libxtst6 libxi6 libgtk-3-0 \
    xauth \
 && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
 && locale-gen en_US.UTF-8 ja_JP.UTF-8 \
 && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV TZ=$TZ

# ROS 2 リポジトリ追加（Humble）
RUN apt-get update && apt-get install -y curl gnupg2 lsb-release \
 && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/ros2.list \
 && apt-get update
# ROS 2 Humble と開発ツール
RUN apt-get install -y \
    ros-humble-desktop \
    ros-humble-topic-tools \
    ros-humble-rmw-fastrtps-cpp \
    ros-humble-rmw-cyclonedds-cpp \
    python3-rosdep python3-colcon-common-extensions python3-vcstool \
    python3-argcomplete \
    # 画像/点群があるなら便利パッケージ（任意）
    ros-humble-image-transport \
    ros-humble-cv-bridge \
    ros-humble-perception-pcl \
 && rm -rf /var/lib/apt/lists/*

# ユーザ作成（UID/GID をホストと合わせると便利）
RUN groupadd -g ${GID} ${USERNAME} \
 && useradd -m -s /bin/bash -u ${UID} -g ${GID} ${USERNAME} \
 && usermod -aG sudo,video,render ${USERNAME} \
 && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# rosdep 初期化（root）→ update（ユーザ）
RUN rosdep init || true
USER ${USERNAME}
WORKDIR /home/${USERNAME}
RUN rosdep update || true

# ROS 2 環境を bashrc に追記
COPY fastdds.xml /home/${USERNAME}
ENV FASTDDS_DEFAULT_PROFILES_FILE=/home/${USERNAME}/fastdds.xml
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# OpenGL/X11の環境変数（必要に応じて）
ENV LIBGL_ALWAYS_INDIRECT=0
ENV EGL_PLATFORM=x11
ENV __GL_YIELD=USLEEP
ENV __GL_SYNC_TO_VBLANK=0

# RMW は必要に応じて切替（コメントを外す）
# ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp

# NVIDIA ランタイム利用時のヒント用（ホスト側で nvidia-container-toolkit が必要）
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

CMD ["/bin/bash"]
