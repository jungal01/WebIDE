FROM ubuntu:18.04

WORKDIR /app

COPY . /app

RUN apt-get -y update

RUN apt-get install -y python3

RUN apt-get -y install python3-pip

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["./server/app.py"]
