FROM mcr.microsoft.com/devcontainers/python:3-bookworm

# [Optional] Install additional OS packages
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <packages-web>

# Install Python dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r //tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
