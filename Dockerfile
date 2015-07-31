# Learning from: https://www.digitalocean.com/community/tutorials/docker-explained-how-to-containerize-python-web-applications
# Info also from: http://docs.resin.io/#/pages/configuration/resin-base-images.md

FROM resin/edison-python:latest

ENV INITSYSTEM on

# https://github.com/intel-iot-devkit/upm/blob/master/docs/building.md
RUN git clone https://github.com/intel-iot-devkit/upm.git && \
    cd upm && \
    mkdir build && \
    cd build && \
    cmake .. -DBUILDSWIGNODE=OFF && \
    make && \
    make install

ADD /mredison /mredison

RUN pip install -r /mredison/requirements.txt

WORKDIR /mredison

# How to get the absolute path out of this?
CMD ["./startscript.sh"]
