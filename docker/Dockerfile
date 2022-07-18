FROM python:3.10

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false --local
COPY ./fastflows /app/fastflows
COPY ./flows /app/flows
RUN ls /app
COPY ./README.md /app
COPY ./pyproject.toml /app

RUN poetry install --no-dev

EXPOSE 80

CMD ["uvicorn", "fastflows.main:app", "--host", "0.0.0.0", "--port", "80"]
