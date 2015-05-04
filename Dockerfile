FROM ubuntu:15.04
MAINTAINER mckeimic <docker@mckeimic.com>

RUN apt-get update && apt-get install -y \
python \
python-pip \
python-dev \
redis-cli \
redis-server

ADD . /redirector
RUN pip install -r /redirector/requirements.txt
EXPOSE 80
WORKDIR /redirector
CMD [ "redis-server", "&&", "python", "redirect.py"]
