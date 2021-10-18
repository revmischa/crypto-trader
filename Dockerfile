FROM arm64v8/python:3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
PYTHONHASHSEED=random \
PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc libffi-dev g++ \
    build-essential wget git rustc libssl-dev libz-dev \
    gfortran python3-dev libopenblas-dev liblapack-dev \
    libjpeg-dev libtiff-dev libpng-dev python3-venv python3-wheel \
    python3-setuptools

WORKDIR /src
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
RUN tar -zxf ta-lib-0.4.0-src.tar.gz
RUN cd ta-lib  wget 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD' -O config.guess && \
    wget 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD' -O config.sub && \
    ./configure --build aarch64 --prefix=/usr LDFLAGS="-lm"
RUN cd ta-lib && make -j1 && make install
RUN pip3 install -U pip 

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
PIP_DISABLE_PIP_VERSION_CHECK=1 \
PIP_NO_CACHE_DIR=1 \
POETRY_VERSION=1.1.11

RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /src
COPY pyproject.toml poetry.lock /src/
RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip3 install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base AS runtime
COPY --from=builder /runtime /usr/local
COPY run-bot.py /app/
COPY trader /app/trader
WORKDIR /app

CMD python3 run-bot.py
