FROM python:3.7-slim-buster AS compile-image
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

FROM python:3.7-slim-buster AS build-image
COPY --from=compile-image /opt/venv /opt/venv

ENV WAZO_AUTH_CLI_CONFIG=/etc/wazo-auth-cli

COPY ./etc/wazo-auth-cli /etc/wazo-auth-cli
RUN true \
    && mkdir -p /etc/wazo-auth-cli/conf.d

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT ["wazo-auth-cli"]
