# Learning from: https://www.digitalocean.com/community/tutorials/docker-explained-how-to-containerize-python-web-applications
# Info also from: http://docs.resin.io/#/pages/configuration/resin-base-images.md

FROM resin/edison-python:latest

ENV INITSYSTEM on

ADD /mredison /mredison

RUN pip install -r /mredison/requirements.txt

WORKDIR /mredison

CMD ["python", "mredison.py"]