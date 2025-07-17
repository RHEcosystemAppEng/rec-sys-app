FROM registry.access.redhat.com/ubi9/python-311

USER root
WORKDIR /app/

# install and activate env
COPY pyproject.toml pyproject.toml
RUN pip3 install uv
RUN uv pip install -r pyproject.toml
RUN dnf update -y

COPY recsysapp/ recsysapp/
# give premisssions 
RUN chmod -R 777 . && ls -la

ENV HF_HOME=/hf_cache
RUN mkdir -p /hf_cache && \
    chmod -R 777 /hf_cache