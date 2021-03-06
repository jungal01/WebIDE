'''
Author: Kevin Cobble
Date: 5-8-2019
Description:

The purpose of this file is to actually host the overal server that the
application runs on. The bas structure is Flask.

#Function : getfile
This function will take the file that is uploaded from the HTML and initially
check to see if it is a file that is able to be run, this is based off of the
extension of the file. The function then will read the fiile and upload the data,
including language, based on the extension back to the html/javascript. This is
done through the use of the cookie data structure, and JSON.

#Function : allowed_file
This function just checks the extension of the file against a set of allowed
extensions to make sure that the file is readable. It does not output an error,
but later it should be implemented with an error that the user can see.

#Function : index
Calls the initial index page

#Function : aboutPage
An incomplete page that is called. We ran out of time before Eros could
implement it and did not have a chance to remove it.

#Function : compile
A self testing function with try and except statements, that if it produces an
error, it will show it to the user. This is both to catch errors within the
code that is to be executed by the compiler, and within this server itself. It
initially recieves info from a javascript page, including language, code, and
file name. It will then adjust variables based on those variables so that
everything is set up for either the AI to run or not. Whether the AI is run,
or not will not affect the compiler itself. The compiler would be called after
the AI, if it was run. Either way, the server adjusts variables so that the
compiler can run as well. Once it gets information back from the compiler,
it generates an output to be sent back to the website.

#Function : bytecode
This function is ment to be a download function to retrieve the appropriate
byte files that are generated for some languages. However, due to time
limitations, this was not implemented properly and recieved little attention
in comparison to other pieces of the code.


# How to Run
To acces the server based outside of a local host, you must run:
conda activate python37
export FLASK_APP=app.py
flask run --host=0.0.0.0

running the docker is the most effective way to run it if you are running on
local host. Due to time constraits, Jason had me implement
the export method when actually using the school computer.
However, it would not be a complex fix for the docker system. I believe it is
currently set up so that you could, in theory run it just the docker.

However to run it effectively, there is a requirement that you have conda.

'''


import sys
import os
import random
import json
import language
from flask import *
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = set(['txt', 'py', 'js', 'java', 'cpp', 'c', 'rs'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/getfile', methods=['GET', 'POST'])
def getfile():  # Retrieves files that client is uploading
    if request.method == 'POST':
        file = request.files['myfile']
        filename = secure_filename(file.filename)

        file.save(os.path.join("importCode", filename))

        if allowed_file(filename):  # Function call to checks file type against readible types
            with open("./importCode/"+filename) as f:
                file_content = f.read()
                f.close()
            fileInfo = filename.rsplit('.', 1)[0]+"=."+filename.rsplit('.',1)[1].lower()+":::"+file_content
            print(filename)
            print(file_content)
            print(fileInfo)
            return render_template('index.html', fileContent=file_content, uploadedName=filename, data = fileInfo)

    return render_template('index.html', data="Error=AI:Failure to load File")


def allowed_file(filename):  # Checks file type
    extension = filename.rsplit('.', 1)[1].lower()
    if ('.' in filename and extension in ALLOWED_EXTENSIONS):
        return True
    return False


@app.route('/')
def index():  # Serves up index template
    print("Rendering index html")
    return render_template('index.html')


@app.route('/about')
def aboutPage():  # Serves up about template
    print("Rendering about html")
    return render_template('about.html')


@app.route('/compile', methods=['POST'])
def compile():  # Takes code from JS and returns output to JS
    os.system("echo ''>errFile.txt")
    os.system("echo ''>output.txt")
    version = None
    err = ''
    print("Got code run request")
    if request.method == "POST":
        code = request.form['param1']
        lang = request.form['param2']
        name = request.form['param3']
    print("Got code, language or api, name")
    print("Code: "+code)
    print("Lang or AI: "+lang)
    print("Name: "+name)

    try:  # Try to call the specific language
        if lang != 'AI':
            if lang == '.js':
                version = 'js'
            elif lang == '.java':
                version = 'java'
            elif lang == '.c':
                version = 'c'
            elif lang == '.cpp':
                version = 'cpp'
            elif lang == '.py':
                version = 'python'
            elif lang == '.rs':
                version = 'rust'
            elif lang == '.rb':
                version = 'ruby'
            elif lang == '.sh':
                version = 'bash'
            elif lang == '.lua':
                version = 'lua'
            elif lang == '.go':
                version = 'go'
            elif lang == '.f90':
                version = 'fortran'
            elif lang == '.m':
                version = 'objc'
            elif lang == '.mm':
                version = 'objcpp'
            elif lang == '.adb':
                version = 'ada'
            else:
                raise Exception("Language not supported")
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("LANGUAGE ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try:  # Try to call the API
        if lang == 'AI':
            # Call AI
            lang = '.txt'
            with open(name+lang, 'w') as f:
                f.write(code)
            version, confidence = language.identify(name+lang)
            version = version.lower()
            print("Identified language as: "+version)
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("API ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try:  # get language from version, from API
        if lang == '.txt':
            if version == 'java':
                lang = '.java'
            elif version == 'javascript':
                version = 'js'
                lang = '.js'
            elif version == 'c':
                lang = '.c'
            elif version == 'python':
                lang = '.py'
            elif version == 'rust':
                lang = '.rs'
            elif version == 'lua':
                lang = '.lua'
            elif version == 'c++':
                version = 'cpp'
                lang = '.cpp'
            elif version == 'go':
                lang = '.go'
            elif version == 'objective-c':
                version = 'objc'
                lang = '.m'
            elif version == 'ruby':
                lang = '.rb'
            elif version == 'shell':
                version = 'bash'
                lang = '.sh'

            else:
                # version = language.identify(code)
                raise Exception("Language is not supported")
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("VERSION ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try:  # Try to write the code file
        with open(name+lang, 'w') as f:
            f.write(code)
            f.close
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("WRITING ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try:  # Create & send response to send to javascript
        os.system("./call-compiler {} {}".format(version, name+lang))
        with open('output.txt', 'r') as f:
            result = lang+":::" + f.read()
            f.close()

        print('results: '+result)
        if result == lang or result == '\n':
            raise Exception("COMPILE ERROR: Empty file output.txt")
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("RESPONSE ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))
        result = str(e)

    os.system("rm {}".format(name+lang))
    return make_response(result)


@app.route('/bytecode', methods=['POST'])
def bytecode():  # looks for specific executables and then returns their contents to JS for download
    exclude = ['call_compiler']
    fileNames = ['cclang', 'ccpp', 'cgo', 'cObjcpp', 'cObjc', 'crust', 'cfortran']
    version = None
    print("Got code bytecode request")
    if request.method == "POST":
        lang = request.form['param1']
        name = request.form['param2']
    print("Got code, language or api, name")
    print("Lang or AI: " + lang)
    print("Name: " + name)
    if lang == '.java':
        try:
            with open(name+'.class', 'rb') as f:
                result = [name+'.class', f.read()]
        except Exception:
            pass
    elif lang == '.adb':
        try:
            with open(name, 'rb') as f:
                result = [name, f.read()]
        except Exception:
            pass
    else:
        for file in fileNames:
            try:
                with open(file, 'rb') as f:
                    result = [file, f.read()]
            except Exception:
                pass
    return make_response(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True, host=('0.0.0.0'))
