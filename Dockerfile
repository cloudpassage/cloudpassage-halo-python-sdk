FROM alpine:3.4
MAINTAINER toolbox@cloudpassage.com

RUN apk add -U \
    gettext \
    python \
    py-pip && \
    apk add --no-cache git

COPY ./ /source/

WORKDIR /source/

RUN pip install -r requirements-testing.txt && \
    pip install -e .

RUN pip install codeclimate-test-reporter

CMD /source/test_wrapper.sh
