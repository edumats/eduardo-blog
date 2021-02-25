FROM python:3.9-slim-buster

WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy all files to current directory
COPY . .
