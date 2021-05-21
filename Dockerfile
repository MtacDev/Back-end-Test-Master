#!/bin/bash

FROM python:3.8

ENV PYTHONNUNBUFFERED = 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN python -m pip install -r requirements.txt

COPY . /code/

CMD ["python","-u","cornershop-backend-test/views.py"]


