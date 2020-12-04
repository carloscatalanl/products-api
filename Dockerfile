FROM python:3.10.0a2-alpine3.12

WORKDIR /app

COPY requirements.txt /app

RUN pip3 --no-cache-dir install -r requirements.txt