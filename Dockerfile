# Copyright 2019 YAM AI Machinery Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
