FROM python:3.8
LABEL maintainer="Florian Sabani"
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV POSTGRES_USER=test
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_HOST=192.168.1.110
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=example

ENV FLASK_APP=src/example/app.py

EXPOSE 5000

CMD [ "flask", "run" ]
