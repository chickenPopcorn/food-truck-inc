FROM python:2.7

RUN mkdir -p /app

WORKDIR /app

ADD . /app

RUN cd /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "/app/server.py"]
