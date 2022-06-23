FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV MAKEFLAGS -j4

RUN apt-get -q update \
    && apt-get -q -y upgrade

WORKDIR /srv/roads

COPY ./src/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip wheel \
    && pip install --no-cache-dir -r requirements.txt

RUN apt-get -q -y autoremove \
    && apt-get -q -y clean \
    && apt-get -q -y autoclean

COPY ./src/. ./

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
