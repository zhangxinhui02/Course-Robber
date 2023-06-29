FROM python:slim

COPY Src /app
WORKDIR /app
VOLUME /app/config

CMD python main.py

