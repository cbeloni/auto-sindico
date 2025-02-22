FROM python:3.12.9-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN apt-get update
RUN apt-get install -y build-essential python3-greenlet pip git wget libgdal-dev
RUN pip install pipenv 
# COPY Pipfile Pipfile.lock ./
COPY . .
RUN pip install --upgrade pip pipenv
RUN echo "iniciando o instalacao dependências"
RUN pipenv install --deploy --system --verbose
RUN echo "iniciando o pipenv run..."
ENTRYPOINT ["pipenv", "run", "python3", "main.py"]
