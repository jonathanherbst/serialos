FROM mcr.microsoft.com/devcontainers/base:ubuntu24.04

# install packages required for yocto
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    chrpath \
    cpio \
    debianutils \
    diffstat \
    file \
    gawk \
    gcc \
    git \
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
    socat \
    texinfo \
    unzip \
    wget \
    xz-utils \
    zstd

# setup the locale as required by yocto
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen
