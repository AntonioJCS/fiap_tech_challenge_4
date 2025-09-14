FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.api.main_public:app", "--host", "0.0.0.0", "--port", "8000"]