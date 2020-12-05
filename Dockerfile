FROM python:3

WORKDIR /app

COPY requirements.txt /app

RUN pip3 --no-cache-dir install -r requirements.txt