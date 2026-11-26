FROM python:3.13-slim
LABEL maintainer="Frojd"
LABEL version="v0.1.0"

ENV PYTHONUNBUFFERED=1 \
    APP_LOG_DIR=/var/log/app

RUN apt-get update \
    && apt-get install -y netcat-traditional \
		binutils libproj-dev gdal-bin \
		gettext \
		libpq-dev build-essential \
		--no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --create-home app \
    && mkdir -p $APP_LOG_DIR \
    && chown app:app $APP_LOG_DIR

COPY --chown=app:app . /app/
WORKDIR /app

RUN pip install --upgrade pip \
    && pip install -e .[test] --no-cache-dir \
    && pip install psycopg2-binary==2.9.10 \
    && pip install ipython \
    && pip install pywatchman \
    && pip install python-dotenv

USER app

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["runserver"]
