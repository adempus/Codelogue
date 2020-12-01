FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
# copy project contents
COPY . /server
# copy project dependencies file
COPY pyproject.toml poetry.lock* /server/
WORKDIR /server
# install project dependencies
RUN poetry install --no-root --no-dev
CMD ["export FLASK_ENV=development", "export FLASK_APP=main", "flask run"]

EXPOSE 5001
