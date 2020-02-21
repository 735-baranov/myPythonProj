FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY . /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

# expose a port for the flask development server
EXPOSE 5000

#ENTRYPOINT ["/bin/sh"]
ENTRYPOINT ["python3"]
CMD ["main.py"]
