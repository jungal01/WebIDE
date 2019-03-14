import os

print(str(os.system('docker run hello-world')))
print('~'*25)
print(str(os.system('docker info')))
print('~'*25)
os.system('docker purge')
print('~'*25)
print(str(os.system('docker info')))
def print(file):
    with open(file, 'r') as f:
        pass