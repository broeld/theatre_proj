FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Theatre_proj

COPY Pipfile Pipfile.lock /Theatre_proj/
RUN pip install pipenv && pipenv install --system

COPY . /Theatre_proj
