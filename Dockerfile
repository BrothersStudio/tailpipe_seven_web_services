FROM python:3.6-slim

MAINTAINER BrothersGameStudio@gmail.com

ARG input

COPY scripts/ /src/scripts
COPY requirements.txt /src/

RUN pip3 install -r /src/requirements.txt

EXPOSE 5000

CMD ["python", "/src/scripts/app.py", "-p 5000"]