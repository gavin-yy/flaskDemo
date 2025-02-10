FROM python

LABEL description="python with docker"


RUN apt-get update && \
    apt-get install redis-server -y &&\
    apt-get install redis-sentinel

RUN echo 'build complete'
