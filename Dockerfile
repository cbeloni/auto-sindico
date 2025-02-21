FROM ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /
COPY . .
RUN apt-get update
RUN apt-get install -y pip git wget
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile
# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.server:app"]
ENTRYPOINT ["python3","main.py"]
