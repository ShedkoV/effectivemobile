ARG python_version=3.9

FROM python:${python_version}-slim AS python-base

ARG test

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.0 \
    POETRY_HOME="/etc/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/etc/pysetup" \
    VENV_PATH="/etc/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.7.0

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml ./

# Проверка установки Poetry
RUN poetry --version

RUN poetry install

FROM python-base as production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR /backend
ENV PYTHONPATH=/backend/src

ARG rebuild

RUN echo ${rebuild}

COPY . .

CMD ["uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
