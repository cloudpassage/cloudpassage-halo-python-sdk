ARG PY_VER=2.7.10
FROM docker.io/halotools/python_tester:${PY_VER}
LABEL maintainer="toolbox@cloudpassage.com"

COPY ./ /source/

WORKDIR /source/

RUN /opt/python/bin/python -mpip install -r requirements-testing.txt && \
    /opt/python/bin/python -mpip install -e .
