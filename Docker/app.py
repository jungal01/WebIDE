# within the test file, there is a test application that runs the entire server within a docker container
from flask import Flask, render_template
import os

app = Flask(__name__)

# Just is used to quickly read and return a string for the server to display on the webpage
def read_output(file):
    with open(file, 'r') as f:
        data = f.read()
    print(data)
    return data

@app.route('/')
def hello_world():
    # Starts a docker and runs the hello world that comes with docker. Runs the docker container with the id/name of Hello, so it can be stopped
    os.system("docker run -name='Hello' hello-world > hello.txt")
    hello = read_output('hello.txt')
    # currently non functioning, but should stop the container named hello However, it does not return an output if this is done, though it does appear to stop
    # os.system('docker stop hello')
    # this is the command to remove a docker container
    #os.system('docker rm hello')
    # I was using the info.txt to actually see if the docker was running or not
    os.system('docker info > info.txt')
    info = read_output('info.txt')
    
    return hello + info
# Nothing about the hellow-world gets displayed if the docker is named, after the first time around. If it keeps getting refresshed it doesnt show anything. Should there be no name
# and no removal of dockers or stoppage of the docker, you can run it as many times as you want, but each time
# it creates a new docker and keeps the old ones running
if __name__=='__main__':
    app.run(debug=True, host = '0.0.0.0')