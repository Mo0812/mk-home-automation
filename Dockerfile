FROM python:3.8.5-slim

RUN apt-get -y update && apt-get -y upgrade && apt install -y libomp-dev libgomp1

ENV PYTHONUNBUFFERED=TRUE

RUN pip --no-cache-dir install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --system && rm -rf /root/.cache

RUN mkdir -p model
COPY [".env.docker", "./.env"]
COPY ["app/*.py", "./"]
COPY ["app/model/*", "./model/"]

RUN ls -la

EXPOSE 9090

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9090", "server:app"]