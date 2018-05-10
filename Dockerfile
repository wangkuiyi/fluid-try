# This Docker image is the development environment that is used to
# build Fluid from source code.
FROM nvidia/cuda:9.1-cudnn7-devel-ubuntu16.04
MAINTAINER Yi Wang <yi.wang.2005@gmail.com>

RUN apt-get update
RUN apt-get install -y \
    git \
    cmake coreutils libtool clang llvm clang-format \
    wget curl unzip tar bzip2 gzip \
    automake \
    python-pip python-dev python-protobuf \
    openssh-server \
    sed grep gawk net-tools \
    zlib1g-dev  \
    liblapack-dev liblapacke-dev
RUN apt-get install -y protobuf-compiler libprotobuf-dev
RUN apt-get clean -y

# git credential to skip password typing
RUN git config --global credential.helper store

RUN pip install pre-commit

# Configure OpenSSH server. c.f. https://docs.docker.com/engine/examples/running_ssh_service
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
EXPOSE 22

# development image default do build work
CMD ["/usr/sbin/sshd", "-D"]
