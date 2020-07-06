#https://hub.docker.com/repository/docker/evansalz/cpsc4973-image-gallery
FROM python:3.7

RUN apt-get update
RUN apt-get install -y gcc postgresql bash git

COPY ${IG_PASSWD_FILE} .

COPY . /app

WORKDIR app

RUN pip3 install -r requirements.txt

RUN chmod +x createDB
RUN sh createDB

EXPOSE 8888

CMD [ "uwsgi", "--ini", "app.ini" ]