FROM python:3.6-slim-buster
MAINTAINER Frojd
LABEL version="v0.1.0"

ENV PYTHONUNBUFFERED=1 \
    REQUIREMENTS=requirements.txt \
    APP_LOG_DIR=/var/log/app

ADD . /app/
WORKDIR /app

RUN apt-get update \
    && apt-get install -y netcat \
		binutils libproj-dev gdal-bin \
		gettext \
		libpq-dev build-essential \
		--no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install -r $REQUIREMENTS --no-cache-dir \
    && pip install ipython \
    && pip install pywatchman

EXPOSE 8080

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["runserver"]
