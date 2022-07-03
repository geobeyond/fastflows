FROM python:3.8

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false --local
COPY ./fastflows /app/fastflows
COPY ./flows /app/flows
RUN ls /app
COPY ./pyproject.toml /app

RUN poetry install --no-dev

CMD ["fastflows", "server"]
