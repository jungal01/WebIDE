from ai.testt import main_test

def identify(file):
    return main_test(file)

def main():
    version = identify('hello.c')
    print(version)
    
if __name__=='__main__':
    main()