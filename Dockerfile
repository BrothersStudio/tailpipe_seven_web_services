FROM python:3.6-slim

MAINTAINER BrothersGameStudio@gmail.com

ARG interview_table_name
ARG mysql_db
ARG mysql_passwd
ARG mysql_user
ARG mysql_endpoint

COPY scripts/ /src/scripts
COPY requirements.txt /src/

RUN pip3 install -r /src/requirements.txt

EXPOSE 5000

ENV INTERVIEW_TABLE_NAME ${interview_table_name}
ENV MYSQL_DB ${mysql_db}
ENV MYSQL_PASSWD ${mysql_passwd}
ENV MYSQL_USER ${mysql_user}
ENV MYSQL_ENDPOINT ${mysql_endpoint}

CMD ["python", "/src/scripts/app.py", "-p 5000"]