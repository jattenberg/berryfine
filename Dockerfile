#DOCKER_BUILDKIT=1 docker build
FROM python:3.10-buster

WORKDIR /app/

RUN apt-get update && apt-get install -y bash gcc python3-dev

ADD requirements.txt /app/

RUN pip install --upgrade pip pip-tools pytest && \
  pip install -r requirements.txt

COPY . .

#RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat .env
RUN meltano install --clean

#ENTRYPOINT ["meltano", "run", "github-to-postgres"]