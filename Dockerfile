FROM python:alpine

WORKDIR /web/
COPY . /web/

RUN pip install -U pip setuptools \
    && pip install -r requirements.txt

ENV PORT=5000
ENV MULTILABEL_CLASSIFIER_ENDPOINT="http://multilabel-classifier/classifier"
RUN echo '#!/usr/bin/env sh' > /serve.sh \
    && echo 'gunicorn -b 0.0.0.0:${PORT} "web:create_app(\"${MULTILABEL_CLASSIFIER_ENDPOINT}\")"' >> /serve.sh \
    && chmod +x /serve.sh

CMD ["/serve.sh"]
