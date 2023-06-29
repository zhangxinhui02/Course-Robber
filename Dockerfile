FROM python:slim

COPY Src /app
COPY LICENSE /app
COPY README.md /app
WORKDIR /app
VOLUME /app/config
RUN pip3 install -r requirements.txt

CMD python main.py

