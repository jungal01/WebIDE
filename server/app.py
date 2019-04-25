import sys, os, random, json
import identify_langauge as language
from flask import *
from werkzeug.utils import secure_filename


app=Flask(__name__)

UPLOAD_FOLDER="/uploads"
ALLOWED_EXTENSIONS = set(['txt','py','js','java','cpp','c','rs'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':
        #file = request.form['param1']
        file= request.files['myfile']
        filename = secure_filename(file.filename)

        file.save(os.path.join("importCode",filename))

        if allowed_file(filename):
            with open("./importCode/"+filename) as f:
                file_content = f.read()
                f.close()
            fileInfo = filename.rsplit('.',1)[0]+"=."+filename.rsplit('.',1)[1].lower()+":::"+file_content
            print(filename)
            print(file_content)
            print(fileInfo)
            return render_template('index.html',fileContent=file_content,uploadedName=filename,data = fileInfo)

    return render_template('index.html',data="Error=AI:Failure to load File")

def allowed_file(filename):
    extension = filename.rsplit('.',1)[1].lower()
    if ('.' in filename and extension in ALLOWED_EXTENSIONS):
        return True
    return False

@app.route('/')
def index(): #Serves up index template
    print("Rendering index html")
    return render_template('index.html')

@app.route('/about')
def aboutPage(): #Serves up about template
    print("Rendering about html")
    return render_template('about.html')

@app.route('/compile', methods=['POST'])
def compile(): #Takes code from JS and returns output to JS
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

    try: # Try to call the specific language
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
                #version = language.identify(code)
                raise Exception("Language not supported")
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("LANGUAGE ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try: # Try to call the API
        if lang=='AI':
            #if lang != None:
            #raise Exception("Language entered and API detection requested")
            ##Call AI
            lang = '.txt'
            version = language.identify(filename+lang)
            print("Identified language as: "+version)

    except Exception as e:
        os.system("echo {} >> errFile.txt".format("API ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try: # get language from version, from API
        if lang == '.txt':
            if version == 'java':
                lang = '.java'
            elif version == 'js':
                lang = '.js'
            elif version == 'c':
                lang = '.c'
            elif version == 'cpp':
                lang = '.cpp'
            elif version == 'python':
                lang='.py'
            elif version == 'rust':
                lang = '.rs'
            else:
                #version = language.identify(code)
                raise Exception("Language is not supported")
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("VERSION ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))


    try: # Try to write the code file
        with open(name+lang, 'w') as f:
            f.write(code)
            f.close
    except Exception as e:
        os.system("echo {} >> errFile.txt".format("WRITING ERROR: "))
        print(e)
        os.system("echo {} >> errFile.txt".format(e))
        os.system("echo {} >> errFile.txt".format('\n'))

    try: # Create & send response to send to javascript
        os.system("./call-compiler {} {}".format(version, name+lang))
        with open('output.txt', 'r') as f:
            result =lang+":::"+ f.read()
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

@app.route('/bitecode', methods=['POST'])
def bitecode():
    exclude = ['call_compiler']
    fileNames = ['cclang','ccpp','cgo','cObjcpp', 'cObjc','crust','cfortran']
    version = None
    print("Got code bitcode request")
    if request.method == "POST":
        lang = request.form['param1']
        name = request.form['param2']
    print("Got code, language or api, name")
    print("Lang or AI: "+lang)
    print("Name: "+name)
    if lang == '.java':
        try:
            with open(name+'.class','rb') as f:
                result = [name+'.class',f.read()]
        except Exception:
            pass
    elif lang == '.adb':
        try:
            with open(name,'rb') as f:
                result = [name,f.read()]
        except Exception:
            pass
    else:
        for file in fileNames:
            try:
                with open(file,'rb') as f:
                    result = [file,f.read()]
            except Exception:
                pass
    return make_response(result)


if __name__== '__main__':
    app.run(debug=True, port=5000, threaded=True, host=('0.0.0.0')) #, host='127.0.0.1', port=5000
