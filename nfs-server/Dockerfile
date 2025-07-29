FROM debian:12

RUN apt-get update
RUN apt-get install -y \
    nfs-ganesha \
    nfs-ganesha-vfs \
    sudo

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${USER_ID} serialos && \
    useradd -N -m -u ${USER_ID} -g ${GROUP_ID} -s "/bin/bash" serialos && \
    adduser serialos sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir /var/run/ganesha
RUN mkdir /run/sendsigs.omit.d/
RUN mkdir /nfs/

COPY ganesha.conf /etc/ganesha/ganesha.conf
