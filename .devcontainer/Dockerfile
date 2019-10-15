FROM ubuntu:18.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Or your actual UID, GID on Linux if not the default 1000
# ARG USERNAME=vscode
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    # 
    # Verify git, process tools, lsb-release (useful for CLI installs) installed
    && apt-get -y install git procps lsb-release \
    #
    # Install C++ tools
    && apt-get -y install build-essential cmake cppcheck valgrind \
    #
    && apt-get install -y sudo
    #
    # Clean up
    # && apt-get autoremove -y \
    # && apt-get clean -y \
    # && rm -rf /var/lib/apt/lists/*
    
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
#ENV PATH /opt/conda/bin:$PATH


RUN apt-get update --fix-missing && \
    apt-get install -y curl python3.6 python3.6-dev python3-pip wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion iproute2 git libncurses-dev flex bison gperf cmake ninja-build ccache gawk grep gettext automake bison flex texinfo help2man libtool libtool-bin make unzip && \
    apt-get clean

RUN  rm /usr/bin/python && \
    ln -s /usr/bin/python3.6 /usr/bin/python 


#RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.7.10-Linux-x86_64.sh -O ~/miniconda.sh && \
#    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
#    rm ~/miniconda.sh && \
#    /opt/conda/bin/conda clean -tipsy && \
#    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
#    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
#    echo "conda activate base" >> ~/.bashrc && \
#    find /opt/conda/ -follow -type f -name '*.a' -delete && \
#    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
#    /opt/conda/bin/conda clean -afy

#RUN conda update -n base -c defaults conda
#RUN conda create -n py3 python=3.7
# RUN /bin/bash -c '. activate py3 && pip install esptool setuptools serial click cryptography future pyparsing==2.3.1 pyelftools'
#RUN /bin/bash -c '. activate py3 && pip install esptool setuptools pyserial click cryptography future pyparsing==2.3.1 pyelftools'
RUN pip3 install esptool pylint micropy-cli setuptools pyserial click cryptography future pyparsing==2.3.1 pyelftools mpfshell-lite

#RUN /bin/bash -c '. activate py3 && pip install --upgrade pyparsing==2.3.1'

# otherwise configure gdb will crash
# RUN mv /opt/conda/envs/py3/lib/python3.7/config-3.7m-x86_64-linux-gnu/libpython3.7m.a /opt/conda/envs/py3/lib/python3.7/config-3.7m-x86_64-linux-gnu/libpython3.7m.a.bak
RUN mv /usr/lib/python3.6/config-3.6m-x86_64-linux-gnu/libpython3.6m.a /usr/lib/python3.6/config-3.6m-x86_64-linux-gnu/libpython3.6m.a.bak

RUN mkdir -p /esp 

# https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
#git checkout esp32-2019r1 && \

RUN cd /esp && \
    git clone https://github.com/espressif/crosstool-NG.git && \
    cd crosstool-NG && \
    git checkout 6c4433a && \
    ./bootstrap && \
    ./configure --enable-local && \
    make

RUN cd /esp && \
    cd crosstool-NG && \
    make install 

#patch gdb - python3
# ADD crosstool.config /esp/crosstool-NG/samples/xtensa-esp32-elf/crosstool.config
ADD crosstool_old.config /esp/crosstool-NG/samples/xtensa-esp32-elf/crosstool.config

# RUN printf "\nCT_ALLOW_BUILD_AS_ROOT=y\nCT_ALLOW_BUILD_AS_ROOT_SURE=y\nCT_GDB_CROSS_PYTHON=y\nCT_GDB_CROSS_PYTHON_BINARY=\"/opt/conda/envs/py3/bin/python\"\n" >> /esp/crosstool-NG/samples/xtensa-esp32-elf/crosstool.config

RUN cd /esp && \
    cd crosstool-NG && \
    ./ct-ng xtensa-esp32-elf &&\
    CT_ONLY_EXTRACT=y ./ct-ng build

ADD python_gdb_new.patch /esp/crosstool-NG/.build/src/gdb-7.10/python_gdb.patch
ADD 300-gdb.sh.patch /esp/crosstool-NG/300-gdb.sh.patch

RUN cd /esp/crosstool-NG && \
    patch -p0 < 300-gdb.sh.patch && \
    cd /esp/crosstool-NG/.build/src/gdb-7.10 && \
    patch -p0 < python_gdb.patch && \
    cd /esp/crosstool-NG && \
    ./ct-ng build && \
    chmod -R u+w builds/xtensa-esp32-elf

ENV PATH "/esp/crosstool-NG/builds/xtensa-esp32-elf/bin:$PATH"

#Supported git hash (v3.3): 6ccb4cf5b7d1fdddb8c2492f9cbc926abaf230df
#Supported git hash (v4.0-beta1) (experimental): 310beae373446ceb9a4ad9b36b5428d7fdf2705f

RUN cd /esp && \
    git clone -b v3.3 --recursive https://github.com/espressif/esp-idf.git && \
    cd /esp/esp-idf && \
    git submodule update --init --recursive

ENV IDF_PATH /esp/esp-idf

RUN git clone --recurse-submodules https://github.com/micropython/micropython.git /root/micropython

RUN cd /root/micropython && \
    make -C mpy-cross

# RUN /bin/bash -c '. activate py3 && pip uninstall -y serial && rm -rf /opt/conda/envs/py3/lib/python3.7/site-packages/serial && pip install pyserial'
# RUN /bin/bash -c '. activate py3 && pip install --upgrade --force-reinstal pyserial'
ADD lolin32_makefile /root/micropython/ports/esp32/lolin32_makefile

RUN cd /root/micropython/ports/esp32 && \
    ESPIDF=$IDF_PATH make -j4 -f lolin32_makefile


#RUN apt-get update && \
#    apt-get install -y curl software-properties-common
#RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
#RUN apt-get install nodejs
#ARG NODE_VERSION=10
#ADD install_node.sh /root/install_node.sh
#RUN bash /root/install_node.sh --version $NODE_VERSION

ADD checks.py.patch
RUN patch -p0 < checks.py.patch

ADD sudoers /etc/sudoers

ENV SHELL /bin/bash
# script to set environment
ADD bashrc /root/bashrc
RUN chmod 755 /root \
    && chmod 755 /root/bashrc
#WORKDIR $THEIA_RUST_APP_PATH
ENV USER root
# CMD [ "bash", "-rcfile", "/root/bashrc", "-i", "/root/run.sh" ]

#RUN apt-get install git wget libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-click python-cryptography python-future python-pyparsing python-pyelftools cmake ninja-build ccache


#sudo apt-get install build-essential libreadline-dev libffi-dev git pkg-config gcc-arm-none-eabi libnewlib-arm-none-eabi


#RUN apt-get install -y python3-pip

# Switch back to dialog for any ad-hoc use of apt-get
#ADD server-env-setup /root/.vscode-server/server-env-setup

