ARG PYTHON_VERSION=3.8.10

# Builder Image
FROM python:${PYTHON_VERSION}-slim-buster as builder

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip install --upgrade pip pipenv
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Final Image
FROM python:${PYTHON_VERSION}-slim-buster

ENV APP_HOME=/backend-template \
    APP_PORT=8080

RUN mkdir $APP_HOME

WORKDIR $APP_HOME

RUN groupadd -g 1001 backend-template \
    && useradd --no-log-init -r -g backend-template -u 1001 backend-template

RUN apt-get update \
    && apt-get install -yqq --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt ./
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN python download_creds_files.py

RUN chown -R 1001:1001 $APP_HOME

USER 1001

EXPOSE $APP_PORT

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "backend-template.wsgi:application"]
