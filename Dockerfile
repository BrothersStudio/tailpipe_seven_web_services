FROM python:3.6

MAINTAINER BrothersGameStudio@gmail.com

ARG stats_table_name
ARG mysql_db
ARG mysql_passwd
ARG mysql_user
ARG mysql_endpoint

COPY src/ /src/scripts
COPY requirements.txt /src/

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server \
 python-dev \
 default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip3 install -r /src/requirements.txt

EXPOSE 5000
EXPOSE 3306

ENV STATS_TABLE_NAME ${stats_table_name}
ENV MYSQL_DB ${mysql_db}
ENV MYSQL_PASSWD ${mysql_passwd}
ENV MYSQL_USER ${mysql_user}
ENV MYSQL_ENDPOINT ${mysql_endpoint}

CMD ["python", "/src/scripts/app.py", "-p 5000", "--host=0.0.0.0"]



