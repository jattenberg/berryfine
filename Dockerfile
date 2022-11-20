#DOCKER_BUILDKIT=1 docker build
FROM python:3.9-buster

WORKDIR /app/

RUN apt-get update && apt-get install -y bash gcc python3-dev

COPY requirements.txt meltano.yml /app/

RUN pip install --upgrade pip pip-tools pytest && \
  usermod --unlock root && \
  mkdir -p ~/.ssh && \
  chmod 0700 ~/.ssh && \
  pip install -r requirements.txt && \
  meltano install --clean

COPY . .

#RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat .env
#--mount type=bind,source=/tmp,target=/usr

ENTRYPOINT   ["meltano", "run", "github-to-postgres"]
#ENTRYPOINT   ["ls", "-lthsa"]