FROM ubuntu:16.04
MAINTAINER Cap. Hindsight <hindsight@yandex.ru>

RUN apt-get update && \
    apt-get -y install \
        sudo

COPY dcont.sh /dcont.sh

WORKDIR /workspace

