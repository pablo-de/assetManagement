FROM python:3.10-rc-slim-buster

RUN apt-get install -y gcc & apt-get install -y default-libmysqlclient-dev

WORKDIR /app

# Copia los archivos de la app.
COPY . .

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "/app/run.py"]