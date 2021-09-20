FROM ubuntu:21.10

RUN apt-get update && apt-get install -y python3 python3-pip curl

# Use Python 3 for `python`, `pip`
RUN    update-alternatives --install /usr/bin/python  python  /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip     pip     /usr/bin/pip3    1

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
ENV PATH "$PATH:/root/.local/bin/"

# Install Poetry packages (maybe remove the poetry.lock line if you don't want/have a lock file)
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --no-interaction

# Provide a known path for the virtual environment by creating a symlink
RUN ln -s $(poetry env info --path) /var/my-venv

# Clean up project files. You can add them with a Docker mount later.
RUN rm pyproject.toml poetry.lock

# Hide virtual env prompt
ENV VIRTUAL_ENV_DISABLE_PROMPT 1

# Start virtual env when bash starts
RUN echo 'source /var/my-venv/bin/activate' >> ~/.bashrc

COPY . .
