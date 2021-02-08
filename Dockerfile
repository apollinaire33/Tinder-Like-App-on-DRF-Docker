FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev

COPY . /srv/html/app
WORKDIR /srv/html/app

COPY ./requirements.txt /srv/html/app/requirements.txt
RUN pip install -r /srv/html/app/requirements.txt