FROM python:3.12.7-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ffmpeg git \
    build-essential libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /VIP/

WORKDIR /VIP

RUN python -m pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir --upgrade --requirement requirements.txt

CMD python3 -m VIP
