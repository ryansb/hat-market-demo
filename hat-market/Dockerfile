FROM alpine:latest

RUN apk -Uuv add bash python3 py3-pip postgresql-dev gcc python3-dev musl-dev

RUN apk --purge -v del
RUN rm /var/cache/apk/*

RUN mkdir -p /app
WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 5000
