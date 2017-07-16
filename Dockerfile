FROM ubuntu:trusty

ENV LANG en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir -p /usr/src/app
COPY . /usr/src/app/
WORKDIR /usr/src/app

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E1DD270288B4E6030699E45FA1715D88E1DF1F24
RUN su -c "echo 'deb http://ppa.launchpad.net/git-core/ppa/ubuntu trusty main' > /etc/apt/sources.list.d/git.list"

RUN locale-gen en_US.UTF-8 && \
    apt-get update && \
    apt-get install -qy --no-install-recommends \
        python3 \
        python3-pip \
        libffi-dev \
        python3-dev \
        build-essential \
        git \
        git-core \
        libssl-dev && \
    \
    pip3 install --upgrade pip setuptools && \
    pip install pika && \
    pip3 install pika && \
    pip3 install aiohttp && \
    pip3 install -e . && \
    \
    apt-get remove -qy --purge gcc cpp binutils perl && \
    apt-get -qy autoremove && \
    apt-get -q clean all && \
    rm -rf /usr/share/perl /usr/share/perl5 /usr/share/man /usr/share/info /usr/share/doc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/expiringdict
RUN python3 setup.py build && \
    python3 setup.py install

#RUN apt-get update && apt-get install -y git-all

#RUN git clone https://github.com/tymlez/consensus.git /usr/src/tymlezconsensus

WORKDIR /usr/src/app/consensus

RUN python3 setup.py build && \
    python3 setup.py install

VOLUME ["/data"]
WORKDIR /data

ENV BIGCHAINDB_CONFIG_PATH /data/.bigchaindb
ENV BIGCHAINDB_SERVER_BIND 0.0.0.0:9984
# BigchainDB Server doesn't need BIGCHAINDB_API_ENDPOINT any more
# but maybe our Docker or Docker Compose stuff does?
# ENV BIGCHAINDB_API_ENDPOINT http://bigchaindb:9984/api/v1

ENTRYPOINT ["bigchaindb"]

CMD ["start"]
