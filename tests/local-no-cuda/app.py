from flask import Flask, request, render_template, make_response
import json
import os

app = Flask(__name__)


@app.route('/')
def index():

    os.system("echo ''>errFile.txt")
    try:
        os.system('rm view.txt')  # rm for linux and del for windows
    except:
        pass

    return render_template('index.html')


@app.route('/about')
def aboutPage():
    return render_template('index_about')


@app.route('/compile', methods=['POST'])
def compile():
    print('Getting request')
    langError = None
    os.system("echo ''>errFile.txt")
    try:
        os.system('rm view.txt')
    except:
        pass
    view = 'view.txt'

    txt = request.form['codeBox01']
    with open(view, 'w') as f:
        f.write(txt)
        f.close()

    with open(view) as f:
        lang = f.readline()
        version = str(language.identify(name))
        # if statement to create appropriately named file
        name = ""
        if lang == '//java':
            name = 'view.java'
        elif lang == '//c':
            name = 'view.c'
        elif lang == '//cpp':
            name = 'view.cpp'
        elif lang == '//rust':
            name = 'view.rs'
        else:
            langError = "Language not supported"

    if name != "":
        os.system('cat {0} > {1}' .format(f, name))

    if name[-2:] == '.c':
        version = 'c'
    elif name[-4:] == '.cpp':
        version = 'cpp'
    elif name[-3:] == '.py':
        version = 'python3'
    elif name[-3:] == '.rs':
        version = 'rust'
    else:
        langError = "Language not supported"
    # will put this in a while loop if we have multiple names over all from the AI
    with open(name, 'w') as f:
        # rv = ''
        # for line in txt:
            # rv+= line+'\n'
        f.write(txt)
        f.close()
    os.system('bash call-compiler {} {}'.format(version, name))
    errorFile = open('errFile.txt', 'r')
    error = errorFile.read()
    errorFile.close()
    if error != '':
        return render_template("index.html", output='Your code is: '+version+'\n'+error, entered=txt)
    elif langError is not None:
        return render_template("index.html",output='Your code is: '+version+'\n'+langError, entered=txt)
    else:
        pass

    # auto populates if there is no error


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
