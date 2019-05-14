from ai.deeplearning.fileinput import *
from torch.utils.data import DataLoader
from torch.nn.functional import cross_entropy
from ai.deeplearning.model import *
from torch.optim import Adam
from torch.autograd.variable import Variable
from os.path import abspath
from pathlib import Path
import torch
from collections import deque
import numpy as np
from ai.deeplearning.modeltran import TransformerBOW, Transformer
from ai.deeplearning.mixedobj import TransformerBOWMixed
import torch.nn.functional as F
import datetime
import os

"""
The traning script for a few models.
"""

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

def sv(var):
    return var.data.cpu().numpy()


def logprint(logfile, string):
    string = str(string)
    if logfile is not None and logfile != False:
        with open(logfile, 'a') as handle:
            handle.write(string + '\n')
    print(string)


def datetime_filename():
    return datetime.datetime.now().strftime("%m_%d_%h_%H_%M_%S")


def mixedtrain(training_data, validation_data, model, optimizer, starting_epoch, num_epochs, id_str, logfile):
    dq=deque(maxlen=100)
    mldq=deque(maxlen=100)
    atdq=deque(maxlen=100)
    emdq=deque(maxlen=100)
    vatdq=deque(maxlen=100)

    for epoch in range(starting_epoch, num_epochs):
        for i,data_point in enumerate(training_data):
            model.train()
            optimizer.zero_grad()
            input, target= data_point
            # if input_long:
            #     input=input.long()
            # else:
            #     input=input.float()
            # target=target.long()
            if len(target.shape)>1:
                target=target.squeeze(1)

            input=input.cuda()
            target=target.cuda()

            all_loss, lml, lat, lem, lvat, y = model.one_pass(input, target)
            all_loss.backward()

            # y=model(input)
            # loss=cross_entropy(y,target)
            # loss.backward()
            optimizer.step()

            pred_prob=F.softmax(y,dim=1)
            pred=torch.argmax(pred_prob,dim=1)
            hit_percentage=torch.sum(pred==target).item()/target.shape[0]

            dq.appendleft(float(all_loss))
            mldq.appendleft(float(lml.item()))
            atdq.appendleft(float(lat.item()))
            emdq.appendleft(float(lem.item()))
            vatdq.appendleft(float(lvat.item()))

            # if i % 100==0:
            #     print(float(loss.item()))

            if i % 100==0:
                logprint(logfile, "epoch %4d, batch %4d. all: %.6f, ml: %.6f, at: %.6f, em: %.6f, vat: %.6f, hit: %.4f" %
                         (epoch, i, np.mean(dq), np.mean(mldq), np.mean(atdq),np.mean(emdq), np.mean(vatdq), hit_percentage))

            if i % 10000==0:
                # wrap, so that python can del the torch objects
                lall, lml, lat, lem, lvat, lhit=mixedeval(model, optimizer, epoch, i, id_str, validation_data)
                logprint(logfile, "validation epoch %4d, all: %.6f, ml: %.6f, at: %.6f, em: %.6f, vat: %.6f, hit: %.4f" % (epoch, lall, lml, lat, lem, lvat, lhit))


def mixedeval(model, optimizer, epoch, i, id_str, validation_data):
    val_losses = []
    mldq=[]
    atdq=[]
    emdq=[]
    vatdq=[]
    hitdq=[]

    save_model(model, optimizer, epoch, i, id_str)
    for j, data_point in enumerate(validation_data):
        if j < 100:
            model.eval()
            input, target = data_point
            # if input_long:
            #     input=input.long()
            # else:
            #     input = input.float()
            # target = target.long()
            if len(target.shape) > 1:
                target = target.squeeze(1)

            input = input.cuda()
            target = target.cuda()
            all_loss, lml, lat, lem, lvat, y = model.one_pass(input, target)

            val_losses.append(all_loss.item())
            mldq.append(lml.item())
            atdq.append(lat.item())
            emdq.append(lem.item())
            vatdq.append(lvat.item())

            pred_prob=F.softmax(y,dim=1)
            pred=torch.argmax(pred_prob,dim=1)
            hit_percentage=torch.sum(pred==target).item()/target.shape[0]
            hitdq.append(hit_percentage)
        else:
            break
    return np.mean(val_losses), np.mean(mldq), np.mean(atdq), np.mean(emdq), np.mean(vatdq), np.mean(hitdq)



# def mixedtrain(training_data, validation_data, model, optimizer, starting_epoch, num_epochs, id_str, em, at, vat, logfile):
#     dq=deque(maxlen=100)
#     mldq=deque(maxlen=100)
#     atdq=deque(maxlen=100)
#     emdq=deque(maxlen=100)
#     vatdq=deque(maxlen=100)
#
#     for epoch in range(starting_epoch, num_epochs):
#         for i,data_point in enumerate(training_data):
#             model.train()
#             optimizer.zero_grad()
#             input, target= data_point
#             # if input_long:
#             #     input=input.long()
#             # else:
#             #     input=input.float()
#             # target=target.long()
#             if len(target.shape)>1:
#                 target=target.squeeze(1)
#
#             input=input.cuda()
#             target=target.cuda()
#
#             lml, lat, lem, lvat, allloss, backme, y =onepass(model, input, target, em, at, vat)
#             backme.backward()
#
#             # y=model(input)
#             # loss=cross_entropy(y,target)
#             # loss.backward()
#             optimizer.step()
#
#             pred_prob=F.softmax(y,dim=1)
#             pred=torch.argmax(pred_prob,dim=1)
#             hit_percentage=torch.sum(pred==target).item()/target.shape[0]
#
#             dq.appendleft(float(allloss))
#             mldq.appendleft(float(lml))
#             atdq.appendleft(float(lat))
#             emdq.appendleft(float(lem))
#             vatdq.appendleft(float(lvat))
#
#             # if i % 100==0:
#             #     print(float(loss.item()))
#
#             if i % 100==0:
#                 logprint(logfile, "epoch %4d, batch %4d. all: %.6f, ml: %.6f, at: %.6f, em: %.6f, vat: %.6f, hit: %.4f" %
#                          (epoch, i, np.mean(dq), np.mean(mldq), np.mean(atdq),np.mean(emdq), np.mean(vatdq), hit_percentage))
#
#             if i % 10000==0:
#                 # wrap, so that python can del the torch objects
#                 lall, lml, lat, lem, lvat, lhit=mixedeval(model, optimizer, epoch, i, id_str, validation_data, em, at, vat)
#                 logprint(logfile, "validation epoch %4d, all: %.6f, ml: %.6f, at: %.6f, em: %.6f, vat: %.6f, hit: %.4f" % (epoch, lall, lml, lat, lem, lvat, lhit))
#
#
# def mixedeval(model, optimizer, epoch, i, id_str, validation_data, em, at, vat):
#     val_losses = []
#     mldq=[]
#     atdq=[]
#     emdq=[]
#     vatdq=[]
#     hitdq=[]
#
#     save_model(model, optimizer, epoch, i, id_str)
#     for j, data_point in enumerate(validation_data):
#         if j < 100:
#             model.eval()
#             input, target = data_point
#             # if input_long:
#             #     input=input.long()
#             # else:
#             #     input = input.float()
#             # target = target.long()
#             if len(target.shape) > 1:
#                 target = target.squeeze(1)
#
#             input = input.cuda()
#             target = target.cuda()
#             lml, lat, lem, lvat, allloss, _ , y =onepass(model, input, target, em, at, vat)
#             val_losses.append(allloss)
#             mldq.append(lml)
#             atdq.append(lat)
#             emdq.append(lem)
#             vatdq.append(lvat)
#
#             pred_prob=F.softmax(y,dim=1)
#             pred=torch.argmax(pred_prob,dim=1)
#             hit_percentage=torch.sum(pred==target).item()/target.shape[0]
#             hitdq.append(hit_percentage)
#         else:
#             break
#     return np.mean(val_losses), np.mean(mldq), np.mean(atdq), np.mean(emdq), np.mean(vatdq), np.mean(hitdq)
#

def train(training_data, validation_data, model, optimizer, starting_epoch, num_epochs, id_str, logfile, input_long=False):

    dq=deque(maxlen=100)

    for epoch in range(starting_epoch, num_epochs):
        for i,data_point in enumerate(training_data):
            model.train()
            optimizer.zero_grad()
            input, target= data_point
            if input_long:
                input=input.long()
            else:
                input=input.float()
            target=target.long()
            if len(target.shape)>1:
                target=target.squeeze(1)

            input=input.cuda()
            target=target.cuda()
            y=model(input)
            loss=F.cross_entropy(y,target)
            loss.backward()
            optimizer.step()

            pred_prob=F.softmax(y,dim=1)
            pred=torch.argmax(pred_prob,dim=1)
            hit_percentage=torch.sum(pred==target).item()/target.shape[0]

            dq.appendleft(float(loss.item()))
            # if i % 100==0:
            #     print(float(loss.item()))

            if i % 100==0:
                logprint(logfile, "epoch %4d, batch %4d. all: %.6f, hit: %.4f" % (epoch, i, float(loss.item()), hit_percentage))

            if i % 10000==0:
                # wrap, so that python can del the torch objects
                val_loss, hit_percentage=eval(model, optimizer, epoch, i, id_str, validation_data, input_long=input_long)
                logprint(logfile, "validation epoch %4d, all: %.6f, hit: %.4f" % (epoch, val_loss, hit_percentage))


def eval(model, optimizer, epoch, i, id_str, validation_data, input_long=False):
    val_losses = []

    save_model(model, optimizer, epoch, i, id_str)
    for j, data_point in enumerate(validation_data):
        if j < 100:
            model.eval()
            input, target = data_point
            if input_long:
                input=input.long()
            else:
                input = input.float()
            target = target.long()
            if len(target.shape) > 1:
                target = target.squeeze(1)
            input = Variable(input)
            target = Variable(target)
            input = input.cuda()
            target = target.cuda()
            y = model(input)
            loss = cross_entropy(y, target)
            val_losses.append(float(loss.item()))

            pred_prob=F.softmax(y,dim=1)
            pred=torch.argmax(pred_prob,dim=1)
            hit_percentage=torch.sum(pred==target).item()/target.shape[0]

        else:
            break
    return np.mean(val_losses), hit_percentage



def save_model(net, optim, epoch, iteration, savestr):
    epoch = int(epoch)
    task_dir = os.path.dirname(abspath(__file__))
    if not os.path.isdir(Path(task_dir) / "saves" / savestr):
        os.mkdir(Path(task_dir) / "saves" / savestr)
    pickle_file = Path(task_dir).joinpath("saves/" + savestr + "/lan_" + str(epoch) + "_" + str(iteration) + ".pkl")
    with pickle_file.open('wb') as fhand:
        torch.save((net, optim, epoch, iteration), fhand)
    print('model saved at', pickle_file)



def load_model(computer, optim, starting_epoch, starting_iteration, savestr):
    task_dir = os.path.dirname(abspath(__file__))
    save_dir = Path(task_dir) / "saves" / savestr
    highestepoch = 0
    highestiter = 0
    if not save_dir.exists():
        return computer, optim, 0, 0
    for child in save_dir.iterdir():
        try:
            epoch = str(child).split("_")[1]
            iteration = str(child).split("_")[2].split('.')[0]
        except IndexError:
            print(str(child))
        iteration = int(iteration)
        epoch = int(epoch)
        # some files are open but not written to yet.
        if child.stat().st_size > 20480:
            if epoch > highestepoch or (iteration > highestiter and epoch == highestepoch):
                highestepoch = epoch
                highestiter = iteration
    if highestepoch == 0 and highestiter == 0:
        print("nothing to load")
        return computer, optim, starting_epoch, starting_iteration
    pickle_file = Path(task_dir).joinpath(
        "saves/" + savestr + "/lan_" + str(highestepoch) + "_" + str(highestiter) + ".pkl")
    print("loading model at", pickle_file)
    with pickle_file.open('rb') as pickle_file:
        computer, optim, epoch, iteration = torch.load(pickle_file)
    print('Loaded model at epoch ', highestepoch, 'iteartion', iteration)

    return computer, optim, highestepoch, highestiter


def lstm_train():
    """
    Trains a character based LSTM model.
    :return:
    """
    computer=build_model()
    computer.cuda()
    computer.reset_parameters()
    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}

    id_str="LSTM"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    t, v= get_data_set(lan_dic)
    optimizer=Adam(computer.parameters(),lr=0.001)
    tig=TimeSeriesIG(t, lan_dic, 64)
    vig=TimeSeriesIG(v,lan_dic, 64)
    traindl=DataLoader(tig,batch_size=8,shuffle=True,num_workers=8)
    validdl=DataLoader(vig,batch_size=8,shuffle=True,num_workers=8)
    train(traindl, validdl, computer, optimizer, 0, 50, id_str, logfile=logfile)

def bigram_train():
    computer= LSTMWrapper(input_size=10000,
                           hidden_size=128,
                           num_layers=8)
    computer.cuda()
    computer.reset_parameters()
    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}

    id_str="bigramLSTM"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    vocab_size=100
    max_len=50
    bs=64
    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bigram=True)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bigram=True, valid=True)

    # print(tig[1])
    optimizer=Adam(computer.parameters(),lr=0.001)
    train(tig, vig, computer, optimizer, 0, 50, id_str, logfile=logfile)



def bigram_bow_train(load=False, resplit=False):
    computer= BOW_model(hidden_factor=64)
    computer.cuda()
    computer.reset_parameters()

    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}
    t, v= get_data_set(lan_dic, load=not resplit, save=resplit)
    optimizer=Adam(computer.parameters(),lr=0.001)

    id_str="bibow"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    if load:
        computer, optimizer, highestepoch, highestiter = load_model(computer, optimizer, 0, 0, "full")

    vocab_size=100
    max_len=50
    bs=64
    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bigram=True, bow=True)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bigram=True, bow=True, valid=True)

    # print(tig[1])
    optimizer=Adam(computer.parameters(),lr=0.001)
    train(tig, vig, computer, optimizer, 0, 50, id_str, logfile=logfile)



def vocab_lstm_train(load=False, resplit=False):
    vocab_size=5000

    computer= LSTM_vocab(vocab_size=vocab_size)
    computer.cuda()
    computer.reset_parameters()

    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}
    t, v= get_data_set(lan_dic, load=not resplit, save=resplit)
    optimizer=Adam(computer.parameters(),lr=0.001)

    vocabuary = select_vocabulary(vocab_size - 2)
    # turn vocabulary into a look-up dictionary
    lookup = {}
    for index, word in enumerate(vocabuary):
        lookup[word] = index

    id_str="vocablstm"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    if load:
        computer, optimizer, highestepoch, highestiter = load_model(computer, optimizer, 0, 0, id_str)
    else:
        highestepoch=0

    bs=64
    tig=VocabIG(t, lan_dic, vocab_size, lookup)
    vig=VocabIG(v, lan_dic, vocab_size, lookup)
    traindl=DataLoader(tig,collate_fn=pad_collate,batch_size=bs,shuffle=True,num_workers=8)
    validdl=DataLoader(vig,collate_fn=pad_collate,batch_size=bs,shuffle=True,num_workers=8)
    train(traindl, validdl, computer, optimizer, highestepoch, 50, id_str, logfile=logfile, input_long=True)

def vocab_bow_train(load=False, resplit=False):
    vocab_size=5000
    max_len=100

    computer= BOW_vocab(vocab_size=vocab_size)
    computer.cuda()
    computer.reset_parameters()

    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}
    t, v= get_data_set(lan_dic, load=not resplit, save=resplit)
    optimizer=Adam(computer.parameters(),lr=0.001)

    id_str="vocabbow"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    if load:
        computer, optimizer, highestepoch, highestiter = load_model(computer, optimizer, 0, 0, id_str)
    else:
        highestepoch=0

    bs=256
    tig=VocabIGpkl(t, lan_dic, vocab_size, max_len, bow=True)
    vig=VocabIGpkl(v, lan_dic, vocab_size, max_len, bow=True)
    traindl=DataLoader(tig,batch_size=bs,shuffle=False,num_workers=8)
    validdl=DataLoader(vig,batch_size=bs,shuffle=False,num_workers=8)
    train(traindl, validdl, computer, optimizer, highestepoch, 50, id_str, logfile=logfile)


def vocab_bow_train_batch_cache(load=False, resplit=False):
    vocab_size=5000
    max_len=100

    computer= BOW_vocab(vocab_size=vocab_size)
    computer.cuda()
    computer.reset_parameters()

    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}
    t, v= get_data_set(lan_dic, load=not resplit, save=resplit)
    optimizer=Adam(computer.parameters(),lr=0.001)

    id_str="vocabbowbatchpkl"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    if load:
        computer, optimizer, highestepoch, highestiter = load_model(computer, optimizer, 0, 0, id_str)
    else:
        highestepoch=0

    bs=256
    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True, valid=True)
    train(tig, vig, computer, optimizer, highestepoch, 50, id_str, logfile=logfile)



def bow_transformer_cache(load=False, resplit=False):
    """
    I am happy with this model.
    I also want to see the performance of the Normal Transformer.
    If necessary, I want to try the different loss functions.
    I want to know why attention did not work.
    :param load:
    :param resplit:
    :return:
    """
    vocab_size=500
    max_len=1000

    computer= TransformerBOW(vocab_size=vocab_size, d_model=128, d_inner=16, dropout=0.1, n_layers=4)
    computer.cuda()
    computer.reset_parameters()

    optimizer=Adam(computer.parameters(),lr=0.001)

    id_str="tranbowsmallvocab" # double all parameters. full vocabulary
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    if load:
        computer, optimizer, highestepoch, highestiter = load_model(computer, optimizer, 0, 0, id_str)
    else:
        highestepoch=0

    # modify batch size here
    bs=256
    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True, valid=True)
    train(tig, vig, computer, optimizer, highestepoch, 50, id_str, logfile=logfile)


def standard_transformer_cache(load=False, resplit=False):
    """
    I am happy with this model.
    I also want to see the performance of the Normal Transformer.
    If necessary, I want to try the different loss functions.
    I want to know why attention did not work.

    It just does not work. The loss does not converge stably. Validation goes to 0.5, 0.2 periodically.
    :param load:
    :param resplit:
    :return:
    """
    vocab_size=500
    max_len=50

    computer= Transformer(vocab_size=vocab_size,max_len=max_len)
    computer.cuda()
    computer.reset_parameters()

    lan_dic={"C":0,
             "C#":1,
             "C++":2,
             "Go":3,
             "Java":4,
             "Javascript":5,
             "Lua":6,
             "Objective-C":7,
             "Python":8,
             "Ruby":9,
             "Rust":10,
             "Shell":11}
    optimizer=Adam(computer.parameters(),lr=0.001)

    id_str="transtd"
    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")

    if load:
        computer, optimizer, highestepoch, highestiter = load_model(computer, optimizer, 0, 0, id_str)
    else:
        highestepoch=0

    # modify batch size here
    bs=64
    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=False)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=False, valid=True)
    train(tig, vig, computer, optimizer, highestepoch, 50, id_str, logfile=logfile, input_long=True)



#
# def mixed_bow_transformer_cache(load=False, resplit=False):
#     """
#     I am happy with this model.
#     I also want to see the performance of the Normal Transformer.
#     If necessary, I want to try the different loss functions.
#     I want to know why attention did not work.
#     :param load:
#     :param resplit:
#     :return:
#     """
#     vocab_size=500
#     max_len=1000
#
#     model= TransformerBOWMixed(vocab_size=vocab_size, d_model=128, d_inner=16, dropout=0.1, n_layers=4)
#     model.cuda()
#     model.reset_parameters()
#
#     optimizer=Adam(model.parameters(),lr=0.001)
#
#     id_str="mixedbow" # double all parameters. full vocabulary
#
#     if load:
#         model, optimizer, highestepoch, highestiter = load_model(model, optimizer, 0, 0, id_str)
#     else:
#         highestepoch=0
#
#
#     logfile = dir_path/("log/" + id_str + "_" + datetime_filename() + ".txt")
#
#     # modify batch size here
#     bs=256
#
#     em=EM()
#     at=AT(model.after_embedding)
#     vat=VAT(model.after_embedding)
#
#     tig=VocabIGBatchpkl(vocab_size=vocab_size, fix_len=max_len, batch_size=bs, bow=True)
#     vig=VocabIGBatchpkl(vocab_size=vocab_size, fix_len=max_len, batch_size=bs, bow=True, valid=True)
#     mixedtrain(tig, vig, model, optimizer, highestepoch,  id_str=id_str, num_epochs=100, em=em, at=at, vat=vat, logfile=logfile)
#
#


def mixed_bow_transformer_cache(load=False):
    """
    :param load: load the newest model available.

    :return:
    """
    vocab_size=500
    max_len=1000

    model= TransformerBOWMixed(vocab_size=vocab_size, d_model=256, d_inner=16, dropout=0.3, n_layers=8,
                               xi=0.5)
    model.cuda()
    model.reset_parameters()

    optimizer=Adam(model.parameters(),lr=0.001)

    id_str="mixedbow3"

    if load:
        model, optimizer, highestepoch, highestiter = load_model(model, optimizer, 0, 0, id_str)
    else:
        highestepoch=0


    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")


    # modify batch size here
    bs=256

    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True, valid=True)
    mixedtrain(tig, vig, model, optimizer, highestepoch,  id_str=id_str, num_epochs=100, logfile=logfile)


def mixed_bow_transformer_cache_2(load=False):
    """
    :param load: load the newest model available.

    :return:
    """
    vocab_size=500
    max_len=1000

    model= TransformerBOWMixed(vocab_size=vocab_size, d_model=256, d_inner=16, dropout=0.2, n_layers=8,
                               xi=0.5, lambda_at=0.3, lambda_vat=0.3)
    model.cuda()
    model.reset_parameters()

    optimizer=Adam(model.parameters(),lr=0.001)

    id_str="mixedbow4" # low lambda. dropout=0.2

    if load:
        model, optimizer, highestepoch, highestiter = load_model(model, optimizer, 0, 0, id_str)
    else:
        highestepoch=0


    logfile = dir_path/("log/"+id_str)
    logfile.mkdir(exist_ok=True)
    logfile=logfile/(id_str + "_" + datetime_filename() + ".txt")


    # modify batch size here
    bs=256

    tig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True)
    vig=VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True, valid=True)
    mixedtrain(tig, vig, model, optimizer, highestepoch,  id_str=id_str, num_epochs=100, logfile=logfile)


if __name__=="__main__":
    standard_transformer_cache()