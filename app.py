from flask import Flask, request, render_template, make_response
import json
import os

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST','GET'])
def compile():
    os.system("echo ''>errFile.txt")
    if request.method == 'GET':
        txt = str(request.args.get('codeBox01'))
        name = str(request.args.get('view'))
    else:
        txt = str(request.form['codeBox01'])
        name = str(request.form['view'])
    #name != cwasm.js, cwasm.wasm, errFile.txt
    if name == 'view.txt':
        #Call AI
        # get version
        # if statement to create appropriately named file
        pass
    elif name[-2:] == '.c':
        version = 'c'
    elif name[-4:] == '.cpp':
        version = 'cpp'
    elif name[-3:] == '.py':
        version = 'python3'
    elif name[-3:] == '.rs':
        version = 'rust'
    else:
        pass
    #will put this in a while loop if we have multiple names over all from the AI
    with open(name,'w') as f:
        f.write(txt)
        f.close()
    os.system('./call-compiler {} {}'.format(version,name))
    rv = ''
    with open('errFile.txt', 'r') as f:
        a = f.read()
        rv = a
        f.close()
        
    if rv != '':
        return redirect(url_for("index",output=rv))
    #auto populates if there is no error
        
if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)        