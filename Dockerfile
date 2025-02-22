FROM python:3.12.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt-get update
RUN apt-get install -y build-essential python3-greenlet pip git wget libgdal-dev
RUN pip install pipenv 

# Copie apenas os arquivos de dependências primeiro
COPY Pipfile Pipfile.lock ./

RUN pipenv install

COPY . .
ENTRYPOINT ["pipenv", "run", "python3", "main.py"]
