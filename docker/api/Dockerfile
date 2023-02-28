FROM python:3.11.1-slim

WORKDIR ../../app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ../api/requirements.txt .
RUN pip install -r requirements.txt
RUN  #pip install "git+git://github.com/samuelcolvin/pydantic@master#egg=pydantic[email,typing_extensions]"
COPY . .