from ai.fileinput import *
from torch.nn.functional import softmax
from ai.model import build_model
from torch.optim import Adam
import torch
from ai.train import load_model

def test(computer, file, lan_dic, verbose=True):
    input=file_to_torch(file, 512)
    output=computer(input)
    val=output[0]
    sm=softmax(val,dim=0)
    pred=torch.argmax(sm).item()
    for key, value in lan_dic.items():
        if value==pred:
            if verbose==True:
                print("The language is",key)
                return key

def main_test(file="testfile"):
    lan_dic={"bash":0,
             "c":1,
             "java":2,
             "python":3}
    computer=build_model()
    optimizer=Adam(computer.parameters(),lr=0.001)
    starting_epoch=0
    starting_iteration=0
    computer, optim, starting_epoch, starting_iteration=load_model(computer,optimizer,starting_epoch,starting_iteration,"simple")
    computer.lstm.flatten_parameters()
    return test(computer,file,lan_dic)

if __name__=="__main__":
    main_test()