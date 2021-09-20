FROM python:3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
PYTHONHASHSEED=random \
PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc libffi-dev g++ build-essential wget git
WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
PIP_DISABLE_PIP_VERSION_CHECK=1 \
PIP_NO_CACHE_DIR=1 \
POETRY_VERSION=1.1.9

RUN wget https://artiya4u.keybase.pub/TA-lib/ta-lib-0.4.0-src.tar.gz
RUN tar -xvf ta-lib-0.4.0-src.tar.gz
RUN cd ta-lib/ && ./configure --prefix=/usr && make && make install

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && poetry install --no-root

COPY . .
RUN . /venv/bin/activate && poetry build

FROM base as final

COPY --from=builder /venv /venv
COPY --from=builder /app/dist .
COPY run-bot.py ./

RUN . /venv/bin/activate && pip install *.whl
CMD ["poetry", "run", "./run-bot.py"]
