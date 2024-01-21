FROM python:3.12.1-bullseye
# FROM python:3.11.1-bullseye

ENV TERM=linux
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYLINTHOME=/var/tmp/pylint
ENV MYPY_CACHE_DIR=/var/tmp/mypy
ENV PYTHONPYCACHEPREFIX=/var/tmp/pycache
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
        mypy \
        Pillow \
        numpy \
        soundfile \
        ffmpeg-python && \
    rm -rf /usr/share/doc/*
