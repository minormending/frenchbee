FROM python:3.10-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir /app
COPY pyproject.toml /app
WORKDIR /app

COPY README.md /app 
RUN mkdir /app/frenchbee
COPY frenchbee /app/frenchbee
RUN poetry install --no-dev

ENTRYPOINT ["frenchbee-cli"]