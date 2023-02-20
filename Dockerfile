FROM python:3.9-slim-bullseye AS compile-image
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /usr/src/wazo-auth-cli/
WORKDIR /usr/src/wazo-auth-cli
RUN pip install -r requirements.txt

COPY setup.py /usr/src/wazo-auth-cli/
COPY wazo_auth_cli /usr/src/wazo-auth-cli/wazo_auth_cli
RUN python setup.py install

FROM python:3.9-slim-bullseye AS build-image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./etc/wazo-auth-cli /etc/wazo-auth-cli
RUN true \
    && mkdir -p /etc/wazo-auth-cli/conf.d \
    # create empty config dir to avoid override system config
    && mkdir -p /root/.config/wazo-auth-cli

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT ["wazo-auth-cli"]
