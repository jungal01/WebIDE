import os
import identify_language as language




#@app.route('/')
#def index():
    #os.system("echo ''>errFile.txt")
    #try:
        #os.system('rm view.txt')
    #except:
        #pass
        
    #return render_template('index.html')

def index():
    os.system("echo ''>errFile.txt")
    try:
        os.system('del view.*')
    except:
        pass
    
    return 'server is listening'


#@app.route('/compile', methods=['POST','GET'])
def compileScript():
    langError = None
    os.system("echo ''>errFile.txt")
    print("ErrFile: ")
    os.system('type errFile.txt')
    print(" :end of ErrFile")
    try:
        os.system('del view.*')
    except:
        pass
    
    method = input("Please enter Method GET or POST: ")
    
    if method == 'GET':# would be request.method
        #txt = str(request.args.get('codeBox01'))
        txt = input("Please enter a basic command: ")
        #name = str(request.args.get('view'))
        name = input("Please enter a name for the file: ")
    else:
        #txt = str(request.form['codeBox01'])
        txt = input("Please enter a basic command: ")
        #name = str(request.form['view'])
        name = 'view.txt'
    #name != cwasm.js, cwasm.wasm, errFile.txt
    if name == 'view.txt':
        #Call AI
        version = 'Unknown'
        with open(name, 'w') as f:
            f.write(txt)        
            
            f.close()
        print('File info: ')
        os.system('type {}'.format(name))
        version = str(language.identify(name))
        print(version)
             
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

        #os.system('copy {} {}'.format(name, newFile))        
            
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
        f.write(txt)
        f.close()
    os.system(' bash call-compiler {} {}'.format(version,name))
    #rv = ''
    #with open('errFile.txt', 'r') as f:
        #a = f.read()
        #rv = a
        #f.close()
        
    #if rv != '':
        #return redirect(url_for("index",output=rv))
    #auto populates if there is no error
    
        
        
def main(): # Client
    
    view = open('view.txt','w')
    view.write('Hello World!')
    view.close()
    os.system('type view.txt')
    print()
    server = index()
    print(server)
    try:
        view = open('view.txt','r')
        view.close()
        print('view.txt found')
    except:
        print('view.txt not found')
        
    compileScript()
    
        
    
        
    
    
    
    
    
if __name__== '__main__':
    #app.run(debug=True, host='0.0.0.0', port=5000)
    main()