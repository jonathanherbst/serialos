FROM debian:12

# install packages required for yocto
RUN apt-get update
RUN apt-get install -y \
    bash-completion \
    build-essential \
    chrpath \
    cpio \
    debianutils \
    diffstat \
    file \
    gawk \
    gcc \
    git \
    iproute2 \
    iputils-ping \
    libacl1 \
    liblz4-tool \
    locales \
    python3 \
    python3-git \
    python3-jinja2 \
    python3-pexpect \
    python3-pip \
    python3-subunit \
    qemu-utils \
    socat \
    sudo \
    texinfo \
    tmux \
    unzip \
    wget \
    xz-utils \
    zstd

# setup the locale as required by yocto
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${USER_ID} megaserial && \
    useradd -N -m -u ${USER_ID} -g ${GROUP_ID} -s "/bin/bash" megaserial && \
    adduser megaserial sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
