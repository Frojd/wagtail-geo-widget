FROM python:3.12-slim
LABEL maintainer="Frojd"
LABEL version="v0.1.0"

ENV PYTHONUNBUFFERED=1 \
    APP_LOG_DIR=/var/log/app

ADD . /app/
WORKDIR /app

RUN apt-get update \
    && apt-get install -y netcat-traditional \
		binutils libproj-dev gdal-bin \
		gettext \
		libpq-dev build-essential \
		--no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install -e .[test] --no-cache-dir \
    && pip install psycopg2-binary==2.9.3 \
    && pip install ipython \
    && pip install pywatchman \
    && pip install python-dotenv

EXPOSE 8080

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["runserver"]
