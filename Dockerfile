FROM python:3.13-alpine

WORKDIR /kubeguardog

COPY requirements.txt .
RUN apk add --no-cache --virtual build-deps tzdata \
    && apk add --no-cache --update curl jq \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -fr requirements.txt \
    && apk del build-deps

COPY src/*.py .

ENV TZ="Europe/Madrid"

ENTRYPOINT ["python3"]
