from flask import Flask, request, render_template, make_response
import json
import os
import identify_language as language

app=Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def aboutPage():
    return render_template('index_about.html')

@app.route('/compile', methods=['POST'])
def compile():
    print('Getting request')
    langError = None
    os.system("echo ''>errFile.txt")
    try:
        os.system('rm view.txt')
    except:
        pass
    #name = 'view.txt'
    #if request.method == 'GET':
        #txt = str(request.args.get('codeBox01'))
        #print(txt)
    name = str(request.args.get('codeName'))
    #else:
        #txt = str(request.form['codeBox01'])
        #name = str(request.form['view'])
    #name != cwasm.js, cwasm.wasm, errFile.txt
    txt = request.form['codeBox01']
    if name == 'view.txt':
        #Call AI
        version = 'Unknown'
        with open(name, 'w') as f:
            f.write(txt)        
            f.close()
        version = str(language.identify(name))
        # if statement to create appropriately named file
        if version == 'java':
            name = 'view.java'
        elif version == 'c':
            name = 'view.c'
        elif version == 'cpp':
            name = 'view.cpp'
        elif version == 'rust':
            name = 'view.rs'
        else:
            langError = "Language not supported"
            
    elif name[-2:] == '.c':
        version = 'c'
    elif name[-4:] == '.cpp':
        version = 'cpp'
    elif name[-3:] == '.py':
        version = 'python3'
    elif name[-3:] == '.rs':
        version = 'rust'
    else:
        langError = "Language not supported"
    #will put this in a while loop if we have multiple names over all from the AI
    with open(name,'w') as f:
        #rv = ''
        #for line in txt:
            #rv+= line+'\n'
        f.write(txt)
        f.close()
    os.system('bash call-compiler {} {}'.format(version,name))
    errorFile = open('errFile.txt','r')
    error = errorFile.read()
    errorFile.close()
    if error != '':
        return render_template("index.html",output='Your code is: '+version+'\n' + error, entered=txt)
    elif langError != None:
        return render_template("index.html",output='Your code is: '+version+'\n' + langError, entered=txt)
    else:
        pass
        
    #auto populates if there is no error
        
if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)    