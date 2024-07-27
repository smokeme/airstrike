FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN mkdir -p /python-docker

CMD [ "python3", "/python-docker/app.py" ]