FROM python:3.12.6-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ffmpeg git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m venv venv \
    && . ./venv/bin/activate \
    && pip install --no-cache-dir --upgrade --requirement requirements.txt

CMD bash -c "source ./venv/bin/activate && python3 -m Vivek"