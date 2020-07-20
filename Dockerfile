FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV MODULE_NAME="app.main"

COPY ./ /app

# install poetry
RUN pip install poetry

# disable virtualenv for peotry
RUN poetry config virtualenvs.create false

# install dependencies
RUN poetry install