# syntax=docker/dockerfile:1
FROM python:3.8
ENV FLASK_APP=src/example/app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV POSTGRES_USER=test
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_HOST__=192.168.1.110
ENV POSTGRES_HOST=172.18.0.1
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=example

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
