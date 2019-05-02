# There is an overfitting issue.
# I want to know which epoch it started happening, and if I should train further.
# The architecture has not saturated at training time.

import os
import csv
from pathlib import Path

def strip(words):
    new_words=[]
    for word in words:
        word=word.strip('.,:')
        new_words.append(word)
    return new_words

def isnum(s):
    try:
        int(s)
        return True
    except ValueError:
        try:
            float(s)
            return True
        except ValueError:
            return False

class Plotter():
    def __init__(self, file):
        self.file=file

        csv_dir_path=os.path.dirname(os.path.abspath(__file__))
        csv_dir_path=Path(csv_dir_path)/"csv"
        csv_dir_path.mkdir(exist_ok=True)
        self.csv_dir_path=csv_dir_path

        self.id_str=self.get_id_str()

        self.log_path=Path(os.path.dirname(os.path.abspath(__file__))).parent / "log"

        self.init_columns()

    def adjust_batch_size(self):
        batch_lookup={
            "LSTM":8,
            "bibow":64,
            "bigramLSTM":64,
            "tranbowsmallvocab":256,
            "transtd":64,
            "vocabbow":256,
            "vocabbowbatchpkl":256,
            "vocablstm":64,
            "mixedbow4":256
        }
        batch_list=self.__getattribute__("batch")
        batch_list=[int(batch)*batch_lookup[self.id_str] for batch in batch_list]
        self.__setattr__("batch",batch_list)

    def init_columns(self):
        self.cols=[]
        with open(self.log_path/self.file, 'r') as f:
            first_line = f.readline()
            words = first_line.split()
            words = strip(words)
            for i in range(len(words)):
                if i % 2 == 0:
                    assert (words[i].isalpha())
                else:
                    assert (isnum(words[i]))
            for i in range(len(words)):
                if i % 2 == 0:
                    coln=words[i]
                    self.cols.append(coln)
                    self.__setattr__(coln, [])
                else:
                    pass

        self.cols_valid=[]
        with open(self.log_path/self.file, 'r') as f:
            for line in f:
                if line.split()[0]!="validation":
                    pass
                else:
                    words=line.split()[1:]

                    words = strip(words)
                    for i in range(len(words)):
                        if i % 2 == 0:
                            assert (words[i].isalpha())
                        else:
                            assert (isnum(words[i]))
                    for i in range(len(words)):
                        if i % 2 == 0:
                            coln = words[i]
                            self.cols_valid.append(coln)
                            self.__setattr__(coln+"_valid", [])
                        else:
                            pass
                    break

    def get_id_str(self):
        id_str=self.file.split("_")[0]
        id_str=id_str.split("/")[0]
        return id_str


    def make_csv(self):
        with open(self.log_path/self.file, 'r') as f:
            for line in f:
                words=line.split()
                words=strip(words)
                if words[0]=="epoch":
                    for i in range(len(words)//2):
                        assert (words[i*2].isalpha())
                        col=words[i*2]
                        thelist=self.__getattribute__(col)
                        thelist.append(words[i*2+1])
                elif words[0]=="validation":
                    words=words[1:]
                    for i in range(len(words)//2):
                        assert (words[i*2].isalpha())
                        col=words[i*2]
                        thelist=self.__getattribute__(col+"_valid")
                        thelist.append(words[i*2+1])
                else:
                    pass
        self.adjust_batch_size()

        n=len(self.__getattribute__(self.cols[0]))
        for col in [self.__getattribute__(col) for col in self.cols]:
            assert(len(col)==n)

        with (self.csv_dir_path/(self.id_str+"_train.csv")).open('w') as f:
            writer = csv.writer(f,  lineterminator='\n')
            writer.writerow(self.cols)
            for i in range(n):
                row=[self.__getattribute__(col)[i] for col in self.cols]
                writer.writerow(row)

        n=len(self.epoch_valid)
        with (self.csv_dir_path/(self.id_str+"_valid.csv")).open('w') as f:
            writer = csv.writer(f,  lineterminator='\n')
            writer.writerow(self.cols_valid)
            for i in range(n):
                row=[self.__getattribute__(col+"_valid")[i] for col in self.cols_valid]
                writer.writerow(row)


        print(self.id_str,"is done")

if __name__ == '__main__':

    files=["LSTM_04_29_Apr_18_17_47.txt","bibow_04_29_Apr_23_43_12.txt","bigramLSTM_04_29_Apr_23_17_46.txt",
           "tranbowsmallvocab_04_30_Apr_00_40_44.txt", "transtd_04_30_Apr_01_43_03.txt", "vocabbow_04_30_Apr_00_34_51.txt",
           "vocabbowbatchpkl_04_30_Apr_00_39_49.txt","vocablstm_04_29_Apr_23_48_56.txt","mixedbow4_04_30_Apr_01_42_08.txt"]
    for i in range(len(files)):
        id_str=files[i].split("_")[0]
        files[i]=id_str+"/"+files[i]
    for file in files:
        plot=Plotter(file)
        plot.make_csv()


# files=[]
# for file in files:
#
#     with open(file,'r') as f:
#         first_line=f.readline()
#         words=first_line.split()
#         words=strip(words)
#         for i in range(len(words)):
#             if i%2==0:
#                 assert(words[i].isalpha())
#             else:
#                 assert(words[i].isnumeric())
#
#
#
#         while True:
#             line=f.readline()
#             if not line:
#                 break
#             words=line.split()
#             if words[3] == "batch":
#                 if words[4] == "0.":
#                     # this is a representation of the epoch
#                     # I just care about running
#                     cod=words[7][:-1]
#                     toe=words[9][:-1]
#                     tt=words[11]
#
#                     line=f.readline()
#                     words=line.split()
#                     sen=words[3][:-1]
#                     spe=words[5][:-1]
#                     roc=words[7][:-1]
#
#                     training_cod.append(cod)
#                     training_toe.append(toe)
#                     training_tt.append(tt)
#                     training_sen.append(sen)
#                     training_spe.append(spe)
#                     training_roc.append(roc)
#
#                     #print("STop here where")
#
#             if words[0] == "model":
#                 if words[2] =="for":
#                     epoch=words[4]
#                     epochs.append(epoch)
#             if words[1] == "validation.":
#                 cod=words[3][:-1]
#                 toe=words[5][:-1]
#                 total=words[7]
#
#                 valid_cod.append(cod)
#                 valid_toe.append(toe)
#                 valid_tt.append(total)
#                 #print("Stop me here")
#
#
#             if words[1] == "validate":
#                 sen=words[3][:-1]
#                 spe=words[5][:-1]
#                 roc=words[7]
#
#                 valid_sen.append(sen)
#                 valid_spe.append(spe)
#                 valid_roc.append(roc)
#
#                 # this is a set of data.
#                 #print("Stop me here")
#     assert(len(training_cod)==len(training_spe))
#     assert(len(training_tt)==len(valid_cod))
#     # assert(len(valid_spe)==len(valid_cod))
#
#     csv_file_name=
#
#     with open(file,"w") as f:
#         f.write("epoch, tcod, ttoe, ttt, tsen, tspe, troc, vcod, vtoe, vtt, vsen, vspe, vroc\n")
#         for i in range(len(training_cod)):
#
#             try:
#                 strs=[]
#                 strs.append(epochs[i])
#                 strs.append(training_cod[i])
#                 strs.append(training_toe[i])
#                 strs.append(training_tt[i])
#                 strs.append(training_sen[i])
#                 strs.append(training_spe[i])
#                 strs.append(training_roc[i])
#
#                 strs.append(valid_cod[i])
#                 strs.append(valid_toe[i])
#                 strs.append(valid_tt[i])
#                 strs.append(valid_sen[i])
#                 strs.append(valid_spe[i])
#                 strs.append(valid_roc[i])
#
#                 newline=", ".join(strs)
#                 f.write(newline+"\n")
#                 #print("Stop")
#             except IndexError:
#                 pass
#
#         f.write("\n")
#
# print("Done")