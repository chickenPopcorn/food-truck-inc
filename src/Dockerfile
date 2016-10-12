# Instructions copied from - https://hub.docker.com/_/python/
FROM python:2.7-onbuild

# tell the port number the container should expose
EXPOSE 5000

RUN pip install -r requirements.txt

# run the command
CMD ["python", "./server.py"]
