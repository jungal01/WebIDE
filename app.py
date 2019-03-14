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
        os.system('rm view.txt') #del for windows, rm for linux
    except:
        pass
    #name = 'view.txt' # used in testing
<<<<<<< HEAD
    name = request.form['codeboxname'] #used in
=======
    name = request.form['codeboxname'] #used in  
>>>>>>> 9ff7d58be84e2c1d1a6d43f34b0e08c85890e821
    print(name)
    txt = request.form['codeBox01']
    try:
        #AI NOT WORK
        #if name == 'view.txt':
            ##Call AI
            #version = 'Unknown'
            #with open(name, 'w') as f:
<<<<<<< HEAD
                #f.write(txt)
=======
                #f.write(txt)        
>>>>>>> 9ff7d58be84e2c1d1a6d43f34b0e08c85890e821
                #f.close()
            #version = str(language.identify(name))
            ## if statement to create appropriately named file
            #if version == 'java':
                #name = 'view.java'
            #elif version == 'c':
                #name = 'view.c'
            #elif version == 'cpp':
                #name = 'view.cpp'
            #elif version == 'rust':
                #name = 'view.rs'
            #else:
                #langError = "Language not supported"
        print('Checking version')
<<<<<<< HEAD
        # Checks what version it is by the name that was entered
=======
>>>>>>> 9ff7d58be84e2c1d1a6d43f34b0e08c85890e821
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
        print('Got Version')
        #will put this in a while loop if we have multiple names over all from the AI Currently its just for one file
        print("opening and writing to the file to create")
        with open(name,'w') as f:
            f.write(txt)
            f.close()
<<<<<<< HEAD

        print("calling compiler")
        os.system('./call-compiler {} {}'.format(version,name)) #bash is used for windows ./ is for linux
        print("Finished compiling")

        errorFile = open('errFile.txt','r')

        error = errorFile.read()
        errorFile.close()

        if error != '': # returns error cases to output if error occured
            return render_template("index.html",output='Your code is: '+version+'\n' + error, inputbox=txt,filename=name)
        elif langError != None:
            return render_template("index.html",output='Your code is: '+version+'\n' + langError, inputbox=txt,filename=name)
        else: # The webassembly should take care of producing the code in the html without having to be passed here
=======
            
        print("calling compiler")
        os.system('./call-compiler {} {}'.format(version,name)) #bash is used for windows ./ is for linux
        print("Finished compiling")
    
        errorFile = open('errFile.txt','r')
        
        error = errorFile.read()
        errorFile.close()
        
        if error != '':
            return render_template("index.html",output='Your code is: '+version+'\n' + error, inputbox=txt,filename=name)
        elif langError != None:
            return render_template("index.html",output='Your code is: '+version+'\n' + langError, inputbox=txt,filename=name)
        else:
>>>>>>> 9ff7d58be84e2c1d1a6d43f34b0e08c85890e821
            pass
            #return render_template("index.html",inputbox=txt, filename=name)
    except UnboundLocalError as e:
        print(e)
        return render_template("index.html",inputbox=txt,filename=name,output=e)
    #auto populates if there is no error

if __name__== '__main__':
<<<<<<< HEAD
    app.run(debug=True, host='127.0.0.1', port=5000)
=======
    app.run(debug=True, host='127.0.0.1', port=5000)    
>>>>>>> 9ff7d58be84e2c1d1a6d43f34b0e08c85890e821
