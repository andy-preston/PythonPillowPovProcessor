FROM python:3.11.1-bullseye

ENV TERM=linux
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        ffmpeg \
        povray povray-includes && \
    apt-get autoremove --purge -y && \
    apt-get clean -y

RUN ln -s /etc/povray /.povray

RUN pip install --upgrade \
        pip && \
    pip install --upgrade \
        git+https://github.com/psf/black \
        Pillow \
        ffmpeg-python && \
    rm -rf /usr/share/doc/*
