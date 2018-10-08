from flask import Flask, request, render_template, make_response
import wtforms
import os

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           output = '')

@app.route('/compile', methods=['GET','POST'])
def compile():
    txt = str(request.form('codeBox01'))
    with open('py-code.py','w') as f:
        print(txt)
        f.write(txt)
        f.close()
    os.system('./call-compiler python py-code.py')
    rv = ''
    with open('py-output.txt', 'r') as f:
        rv = f
        f.close()
    return render_template('index.html', 
                           output = rv)
if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
