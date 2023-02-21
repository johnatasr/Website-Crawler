FROM python:3.9

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "-m" , "main"]