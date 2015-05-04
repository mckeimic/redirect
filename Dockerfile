#FROM ubuntu:14.04
FROM redis
MAINTAINER mckeimic <docker@mckeimic.com>

RUN apt-get update && apt-get install -y \
python \
python-pip \
python-dev

ADD . /redirector
RUN pip install -r /redirector/requirements.txt
EXPOSE 80
WORKDIR /redirector
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf", "&&", "python", "redirect.py"]

#COPY redis.conf /usr/local/etc/redis/redis.conf
#CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
