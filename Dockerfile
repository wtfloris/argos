# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /argos

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install cron vim procps -y && rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt

COPY secrets.py secrets.py
COPY targets.py targets.py
COPY argos.py argos.py

RUN echo "*/5 * * * * root /usr/local/bin/python3 /argos/argos.py > /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/crontab

CMD ["cron", "-f"]

