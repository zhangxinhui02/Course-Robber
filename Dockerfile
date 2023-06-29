FROM python:slim

COPY Src /app
WORKDIR /app
VOLUME /app/config
RUN pip3 install -r requirements.txt

CMD python main.py

