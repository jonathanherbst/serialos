FROM rust:1.88-bookworm

RUN apt-get update
RUN apt-get install -y \
    sudo

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${USER_ID} serialos && \
    useradd -N -m -u ${USER_ID} -g ${GROUP_ID} -s "/bin/bash" serialos && \
    adduser serialos sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN cargo install cargo-nfs3-server

