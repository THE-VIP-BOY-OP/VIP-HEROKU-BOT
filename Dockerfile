FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ffmpeg aria2 \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade --requirement requirements.txt

CMD bash start
