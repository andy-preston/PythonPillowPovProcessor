FROM python:3.11.1-bullseye

ENV TERM=linux
ENV DEBIAN_FRONTEND=noninteractive
ENV PYLINTHOME=/var/tmp
ENV PYTHONPATH=/usr/local/src/imports

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        ffmpeg \
        povray povray-includes && \
    apt-get autoremove --purge -y && \
    apt-get clean -y

RUN ln -s /etc/povray /.povray

RUN pip install --upgrade pip && \
    pip install --upgrade \
        git+https://github.com/psf/black \
        pylint \
        Pillow \
        numpy soundfile \
        ffmpeg-python && \
    rm -rf /usr/share/doc/*
