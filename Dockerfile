FROM python:3.11.5-slim-bullseye

WORKDIR /code

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

