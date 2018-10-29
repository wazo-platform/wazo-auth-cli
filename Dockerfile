FROM python:3.5-slim-stretch

MAINTAINER Wazo Maintainers <dev@wazo.community>

ADD . /usr/src/xivo-auth-cli
WORKDIR /usr/src/xivo-auth-cli
RUN true \
    && apt-get update \
    && apt-get -yqq install git \
    && pip install -r requirements.txt \
    && python setup.py install \
    && apt-get -yqq --autoremove purge git \
    && mkdir -p /etc/wazo-auth-cli/conf.d \
    && touch /etc/wazo-auth-cli/config.yml

ENTRYPOINT ["wazo-auth-cli"]
