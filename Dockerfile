FROM python:3
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

