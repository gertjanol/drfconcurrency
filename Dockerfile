FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /srv/project
WORKDIR /srv/project
ADD requirements.txt /srv/project
RUN pip install -r requirements.txt
ADD . /srv/project
