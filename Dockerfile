FROM ubuntu:latest
LABEL maintainer="imjoseangel"

ARG appname=mlw

RUN mkdir -p /opt/${appname}


RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /opt/${appname}

ADD mlw /opt/${appname}
ADD requirements.txt requirements.txt

RUN pip3 install connexion[swagger-ui]
RUN pip3 install -r requirements.txt

RUN python3 build_database.py

EXPOSE 8080

CMD ["python3", "/opt/mlw/server.py"]
