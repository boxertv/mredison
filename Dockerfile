# Learning from: https://www.digitalocean.com/community/tutorials/docker-explained-how-to-containerize-python-web-applications
# Info also from: http://docs.resin.io/#/pages/configuration/resin-base-images.md

FROM resin/edison-python:latest
MAINTAINER Gergely Imreh <imrehg@gmail.com>

ENV INITSYSTEM on

# Update commit if need to recompile library
ENV UPMCOMMIT ef28607ceadb9868215d703bc8594c5270dca75e
RUN curl -sSL https://github.com/intel-iot-devkit/upm/archive/$UPMCOMMIT.tar.gz \
		| tar -v -C /usr/src -xz && \
    cd /usr/src/upm-$UPMCOMMIT && \
    mkdir build && \
    cd build && \
    cmake .. -DBUILDSWIGNODE=OFF && \
    make && \
    make install

# For caching until requirements.txt changes
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Main code
ADD /mredison /mredison

WORKDIR /mredison

COPY ./*.sh /

CMD ["/docker-entrypoint.sh"]
