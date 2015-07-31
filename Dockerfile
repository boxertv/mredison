# Learning from: https://www.digitalocean.com/community/tutorials/docker-explained-how-to-containerize-python-web-applications
# Info also from: http://docs.resin.io/#/pages/configuration/resin-base-images.md

FROM resin/edison-python:latest
MAINTAINER Gergely Imreh <imrehg@gmail.com>

ENV INITSYSTEM on

ENV UPMCOMMIT 03e72e02f811cb9a47000a6f12fca61a2908d325
RUN curl -sSL https://github.com/intel-iot-devkit/upm/archive/$UPMCOMMIT.tar.gz \
		| tar -v -C /usr/src -xz && \
    cd /usr/src/upm-$UPMCOMMIT && \
    mkdir build && \
    cd build && \
    cmake .. -DBUILDSWIGNODE=OFF && \
    make && \
    make install

# Cached correctly
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD /mredison /mredison

WORKDIR /mredison

COPY ./docker-entrypoint.sh /

CMD ["/docker-entrypoint.sh"]
