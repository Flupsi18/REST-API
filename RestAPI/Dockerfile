FROM python:3.10-alpine

COPY . /RestAPI/
WORKDIR /RestAPI

RUN apk update && \
    apk upgrade
RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python", "start_server.py"]