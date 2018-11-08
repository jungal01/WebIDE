FROM ubuntu:18.04

WORKDIR /app

COPY . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV NAME Hello

CMD ["python3", "app.py"]
