FROM python:3.10-rc-slim-buster

RUN apt update && \
apt install -y gcc libmariadb-dev-compat libmariadb-dev

WORKDIR /app

# Copia los archivos de la app.
COPY . /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]