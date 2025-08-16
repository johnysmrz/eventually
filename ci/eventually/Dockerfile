FROM python:3.13-alpine AS base_stage

LABEL maintainer="Jan Smrz <jan-smrz@jan-smrz.cz>"
LABEL org.opencontainers.image.source="https://github.com/RZB-IT/eventually"
LABEL org.opencontainers.image.title="RZB-IT Eventually"

WORKDIR /app

RUN apk add --no-cache openssh-client git build-base libpq-dev
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN eval "$(ssh-agent -s)"
RUN pip install poetry
COPY . /app

FROM base_stage AS poetry_stage

RUN --mount=type=ssh poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

FROM poetry_stage

HEALTHCHECK CMD [ "curl", "--fail", "--reload", "http://localhost:8080/healthcheck", "||", "exit", "1" ]

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]