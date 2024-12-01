FROM python:3.9.1

ADD . /Backend

WORKDIR /Backend/server

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

RUN pip3 install --no-cache-dir -r ../requirements.txt