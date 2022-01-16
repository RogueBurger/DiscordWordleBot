# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /srv

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg freetype-dev \
    && pip3 install Pillow \
    && apk del build-deps


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt