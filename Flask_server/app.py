from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/_compile',methods=['GET','POST'])
def compile():
    # get the file from the text box
    with open('code.py','w') as f:
        f.write(request.args.get('codeBox01','',type=str))
        f.close()
    # Run compiler
    os.system('call-compiler python code.py')
    # read output file
    with open('py-output.txt','r') as f:
        lines = f.readlines()
        f.close()
    return jsonify(output = lines)

if __name__=='__main__':
    app.run(debug=True, localhost)
# run compiler, pass compiler name, and name of file
# this writes a new file
# take this new file and post AJAX