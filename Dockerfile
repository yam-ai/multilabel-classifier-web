FROM python:alpine

WORKDIR /web/
COPY . /web/

RUN pip install -U pip setuptools \
    && pip install -r requirements.txt

ENV MLC_HOST_PORT="0.0.0.0:5000"
ENV MLC_ENDPOINT="http://0.0.0.0:8000/classifier"
RUN echo '#!/usr/bin/env sh' > /serve.sh \
    && echo 'gunicorn -b ${MLC_HOST_PORT} "web:create_app(\"${MLC_ENDPOINT}\")"' >> /serve.sh \
    && chmod +x /serve.sh

CMD ["/serve.sh"]
