FROM python:3.12-slim

WORKDIR app/

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "app/main_test.py"]
