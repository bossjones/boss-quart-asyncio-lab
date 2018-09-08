FROM ubuntu:bionic

LABEL Maintainer "Malcolm Jones <bossjones@theblacktonystark.com>"

ENV NON_ROOT_USER=developer \
    container=docker \
    TERM=xterm-256color

# SOURCE: https://github.com/ishiland/docker-python-geosupport/blob/9a670fe15ffca194226ce77da13b54014dbe42c3/Dockerfile
# Unable to set GEOFILES and LD_LIBRARY_PATH based on defined geosupport_version. Need additional logic to
# get the name of the `version-18b_` directory.
# ENV PYTHON_PATH=/usr/lib/python$PYTHON_VERSION \
#     PATH="/usr/lib/python$PYTHON_VERSION/bin/:${PATH}" \
#     GEOFILES="/geosupport/version-18b_18.2/fls/"\
#     LD_LIBRARY_PATH="/geosupport/version-18b_18.2/lib/${LD_LIBRARY_PATH}"\
#     geosupport_version=18b

ARG HOST_USER_ID=1000
ENV HOST_USER_ID ${HOST_USER_ID}
ARG HOST_GROUP_ID=1000
ENV HOST_GROUP_ID ${HOST_GROUP_ID}

# libboost-all-dev

RUN sed -i "s,# deb-src http://archive.ubuntu.com/ubuntu/ bionic main restricted,deb-src http://archive.ubuntu.com/ubuntu/ bionic main restricted,g" /etc/apt/sources.list && \
    sed -i "s,# deb-src http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted,deb-src http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted,g" /etc/apt/sources.list && \
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    sudo \
    bash-completion \
    apt-file \
    autoconf \
    automake \
    gettext \
    build-essential \
    ccache \
    curl \
    git \
    lcov \
    libbz2-dev \
    libffi-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    python3-pip \
    vim \
    && \
    \
        apt-get upgrade -yqq && \
        apt-get install -yqq \
        git \
        curl \
        wget \
        curl \
        software-properties-common \
        ca-certificates \
        && \
        locale-gen en_US.UTF-8 && export LANG=en_US.UTF-8 && \
        apt-get update && apt-get install -y --no-install-recommends \
        tcl \
        tk \
        wget \
        curl \
        ca-certificates && \
        apt-get update && apt-get install -y --no-install-recommends \
        bzr \
        git \
        mercurial \
        openssh-client \
        subversion \
        procps && \
        apt-get update && apt-get install -y --no-install-recommends \
        autoconf \
        automake \
        bzip2 \
        file \
        g++ \
        gcc \
        imagemagick \
        libbz2-dev \
        libc6-dev \
        libcurl4-openssl-dev \
        libdb-dev \
        libevent-dev \
        libffi-dev \
        libgeoip-dev \
        libglib2.0-dev \
        libjpeg-dev \
        libkrb5-dev \
        liblzma-dev \
        libmagickcore-dev \
        libmagickwand-dev \
        libmysqlclient-dev \
        libncurses-dev \
        libpng-dev \
        libpq-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libtool \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        libyaml-dev \
        make \
        patch \
        xz-utils \
        zlib1g-dev \
        bash \
        && apt-get autoclean -y && \
        apt-get autoremove -y && \
        rm -rf /var/lib/{cache,log}/ && \
        rm -rf /var/lib/apt/lists/*.lz4


RUN set -xe \
    && useradd -U -d /home/${NON_ROOT_USER} -m -r -G adm,tty,audio ${NON_ROOT_USER} \
    && usermod -a -G ${NON_ROOT_USER} -s /bin/bash -u ${HOST_USER_ID} ${NON_ROOT_USER} \
    && groupmod -g ${HOST_GROUP_ID} ${NON_ROOT_USER} \
    && ( mkdir /home/${NON_ROOT_USER}/.ssh \
    && chmod og-rwx /home/${NON_ROOT_USER}/.ssh \
    && echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key" > /home/${NON_ROOT_USER}/.ssh/authorized_keys \
    ) \
    && echo "${NON_ROOT_USER}     ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && echo "%${NON_ROOT_USER}     ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && cat /etc/sudoers \
    && echo "${NON_ROOT_USER}:${NON_ROOT_USER}" | chpasswd && \
    mkdir /var/run/dbus && \
    mkdir -p /home/${NON_ROOT_USER}/.local/bin && \
    chown ${NON_ROOT_USER}:${NON_ROOT_USER} -Rv /home/${NON_ROOT_USER}

USER ${NON_ROOT_USER}
WORKDIR /home/${NON_ROOT_USER}

ENV LANG C.UTF-8
ENV CI true
ENV PYENV_ROOT /home/${NON_ROOT_USER}/.pyenv
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
ENV PYTHON_CONFIGURE_OPTS="--enable-shared"

RUN curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash && \
    git clone https://github.com/jawshooah/pyenv-default-packages ${PYENV_ROOT}/plugins/pyenv-default-packages && \
    find ${PYENV_ROOT} -name "*.tmp" -exec rm {} \; && \
    find ${PYENV_ROOT} -type d -name ".git" -prune -exec rm -rf {} \;

# RUN PYTHONDONTWRITEBYTECODE=true pyenv install 2.7.14
RUN PYTHONDONTWRITEBYTECODE=true pyenv install --debug 3.7.0

ENV PATH="/home/${NON_ROOT_USER}/.local/bin:${PATH}"
ENV PATH="/usr/lib/ccache:${PATH}"
