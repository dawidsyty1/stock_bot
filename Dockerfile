FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY config/requirements/requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip

# COPY . /usr/src/app
