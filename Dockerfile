# Learning from: https://www.digitalocean.com/community/tutorials/docker-explained-how-to-containerize-python-web-applications
# Info also from: http://docs.resin.io/#/pages/configuration/resin-base-images.md

FROM resin/edison-python:latest
MAINTAINER Gergely Imreh <imrehg@gmail.com>

ENV INITSYSTEM on

# https://github.com/intel-iot-devkit/upm/blob/master/docs/building.md
RUN git clone --depth 1 https://github.com/intel-iot-devkit/upm.git && \
    cd upm && \
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
