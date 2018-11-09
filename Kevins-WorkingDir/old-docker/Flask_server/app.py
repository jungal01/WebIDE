# run: docker build --no-cache -t server .
# in this file. or from the main file run:
# docker build --no-cache -t server -f Flask_server/Dockerfile
# then run: docker run server
# ^^ is currently not working as it creates a python and 
# we need some ubuntu things installed that it wont register if run this way

from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('../angular/static/index.html')

@app.route('/',methods=['GET','POST'])
def compile():
    # get the file from the text box
    with open('/./code.py','w') as f:
        f.write(request.args.get('codeBox01','',type=str))
        f.close()
    # Run compiler
    os.system('/./call-compiler python code.py')
    # read output file
    with open('/./py-output.txt','r') as f:
        lines = f.readlines()
        f.close()
    return jsonify(output = lines)

if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0', port=5000)
# run compiler, pass compiler name, and name of file
# this writes a new file
# take this new file and post AJAX