from ai.deeplearning.plotting.process_log import *
import unittest

class ProcessLogTest(unittest.TestCase):
    def testProcess(self):
        files = ["LSTM_04_29_Apr_18_17_47.txt", "bibow_04_29_Apr_23_43_12.txt", "bigramLSTM_04_29_Apr_23_17_46.txt",
                 "tranbowsmallvocab_04_30_Apr_00_40_44.txt", "transtd_04_30_Apr_01_43_03.txt",
                 "vocabbow_04_30_Apr_00_34_51.txt",
                 "vocabbowbatchpkl_04_30_Apr_00_39_49.txt", "vocablstm_04_29_Apr_23_48_56.txt",
                 "mixedbow4_04_30_Apr_01_42_08.txt"]
        for i in range(len(files)):
            id_str = files[i].split("_")[0]
            files[i] = id_str + "/" + files[i]
        for file in files:
            plot = Plotter(file)
            plot.make_csv()