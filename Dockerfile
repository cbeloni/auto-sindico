FROM python:3.12.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install -y build-essential pip git wget libgdal-dev
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry lock 
RUN poetry install --no-root
ENTRYPOINT ["poetry", "run", "python3", "main.py"]
