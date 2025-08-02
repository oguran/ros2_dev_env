FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive 

# 必要なパッケージインストール
RUN apt-get update && apt-get install -yq \
    build-essential \
    cmake \
    git \
    gdb-multiarch \
    libusb-1.0-0-dev \
    libudev-dev \
    curl \
    python3 \
    python3-pip \
    vim \
    unzip \
    usbutils \
    libhidapi-dev \
    software-properties-common

# GUIサポートとOpenGL/Mesaの追加
RUN apt-get update && apt-get install -yq \
    x11-apps \
    xvfb \
    mesa-utils \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libosmesa6-dev \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# ROS 2リポジトリ追加（公式手順・2024年以降対応）
RUN apt-get update && apt-get install -yq curl gnupg2 lsb-release
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/ros2.list
RUN apt-get update

# ROS2 Jazzy Desktop install
RUN apt-get install -yq \
    ros-humble-desktop \
    ros-dev-tools \
    && rm -rf /var/lib/apt/lists/*

# VS Codeが認識できるようにユーザー作成
RUN useradd -ms /bin/bash dev && cp -r /etc/skel/. /home/dev && chown -R dev:dev /home/dev
# .bash_profileに.bashrcの読み込みを追記
RUN echo 'if [ -f ~/.bashrc ]; then . ~/.bashrc; fi' >> /home/dev/.bash_profile
# devユーザーがsudoでaptコマンドを使えるように設定
RUN apt-get update && apt-get install -y sudo && usermod -aG sudo dev && echo "dev ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# GPU アクセスのためのグループ追加
RUN usermod -a -G video dev

USER dev
WORKDIR /home/dev

# ROS 2環境設定を.bashrcに追加
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Mesa/EGL環境変数の設定
ENV LIBGL_ALWAYS_INDIRECT=0
ENV MESA_GL_VERSION_OVERRIDE=3.3
ENV MESA_GLSL_VERSION_OVERRIDE=330
ENV EGL_PLATFORM=x11
ENV __GL_YIELD="USLEEP"
ENV __GL_SYNC_TO_VBLANK=0

# NVIDIA GPU acceleration settings
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics

CMD ["/bin/bash"]