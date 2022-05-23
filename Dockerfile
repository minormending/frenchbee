FROM python:3.8

RUN mkdir /app 
COPY frenchbee/ /app
COPY pyproject.toml /app 
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENTRYPOINT ["python", "./frenchbee.py"]