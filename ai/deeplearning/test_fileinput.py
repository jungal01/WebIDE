from ai.deeplearning.fileinput import *
import unittest


class TrainTest(unittest.TestCase):
    def test_data_loader(self):
        vocab_size = 500
        max_len = 1000
        bs = 64
        tig = VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs, bow=True)
        data = next(tig)
        self.assertTrue(data[0].shape == (bs, vocab_size))
        self.assertTrue(data[1].shape == (bs,))
        self.assertTrue(isinstance(data[0], torch.FloatTensor))
        self.assertTrue(isinstance(data[1], torch.LongTensor))
        self.assertTrue((data[1] >= 0).all())
        self.assertTrue((data[1] < 12).all())

        tig = VocabIGBatchpkl(vocab_size=vocab_size, max_len=max_len, batch_size=bs)
        data = next(tig)
        self.assertTrue(data[0].shape == (bs, max_len))
        self.assertTrue(data[1].shape == (bs,))
        self.assertTrue(isinstance(data[0], torch.LongTensor))
        self.assertTrue(isinstance(data[1], torch.LongTensor))
        self.assertTrue((data[0] >= 0).all())
        self.assertTrue((data[0] <= vocab_size).all())
        self.assertTrue((data[1] >= 0).all())
        self.assertTrue((data[1] < 12).all())

    def test_training_file_to_vacab(self):
        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}
        train, valid = get_data_set(lan_dic)
        vocab_size = 500
        max_len = 100
        vocabuary = select_vocabulary(vocab_size - 2)
        # turn vocabulary into a look-up dictionary
        lookup = {}
        for index, word in enumerate(vocabuary):
            lookup[word] = index
        for i, data_point in enumerate(train):
            if i > 10:
                break

            i, t = training_file_to_vocab(data_point, lan_dic, vocab_size, lookup, bow=True)
            self.assertTrue(i.shape == (vocab_size,))
            self.assertTrue(t.shape == (1,))
            self.assertTrue((t >= 0).all())
            self.assertTrue((t < 12).all())

            i, t = training_file_to_vocab(data_point, lan_dic, vocab_size, lookup, max_len=max_len)
            self.assertTrue(t.shape == (1,))

            self.assertTrue((i >= 0).all())
            self.assertTrue((i <= vocab_size).all())
            self.assertTrue((t >= 0).all())
            self.assertTrue((t < 12).all())

    def test_TimeSeriesIG(self):
        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}
        train, valid = get_data_set(lan_dic)
        ig = TimeSeriesIG(train, lan_dic, 512)
        for i in range(10):
            print(ig[i])
        ig = TimeSeriesIG(train, lan_dic, 512, bigram=True)
        for i in range(10):
            print(ig[i])
        ig = TimeSeriesIG(train, lan_dic, 512, bow=True)
        for i in range(10):
            print(ig[i])

    def test_VocabIG(self):
        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}
        train, valid = get_data_set(lan_dic)

        vocab_size = 500
        vocabuary = select_vocabulary(vocab_size - 2)
        # turn vocabulary into a look-up dictionary
        lookup = {}
        for index, word in enumerate(vocabuary):
            lookup[word] = index

        ig = VocabIG(train, lan_dic, 500, lookup)
        for i in range(100):
            a = ig[i]
            print(a)

    def test_VocabIGpkl(self):
        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}

        vocab_size = 100
        vocabuary = select_vocabulary(vocab_size - 2)
        # turn vocabulary into a look-up dictionary
        lookup = {}
        for index, word in enumerate(vocabuary):
            lookup[word] = index

        train, valid = get_data_set(lan_dic)
        ig = VocabIGpkl(train, lan_dic, 50000, 100, bow=True)
        ig2 = VocabIG(train, lan_dic, 50000, lookup, bow=True)
        # for i in range(100):
        #     a = ig[i]
        #     print(a)
        a, b = ig[1714]
        a2, b2 = ig2[1714]
        a3, b3 = ig[169714]
        a4, b4 = ig2[169714]
        print("Done")

    def test_VocabIGBatchpkl(self):
        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}
        train, valid = get_data_set(lan_dic)
        ig = VocabIGBatchpkl(vocab_size=500, max_len=100, batch_size=64, bow=False)
        for idx, i in enumerate(ig):
            if idx > 100:
                break
            print(i)

        print("Done")

    def test_pad_sequence(self):
        resplit = False
        vocab_size = 5000

        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}
        t, v = get_data_set(lan_dic, load=not resplit, save=resplit)

        vocabuary = select_vocabulary(vocab_size - 2)
        # turn vocabulary into a look-up dictionary
        lookup = {}
        for index, word in enumerate(vocabuary):
            lookup[word] = index

        tig = VocabIG(t, lan_dic, vocab_size, lookup)
        ll = []
        for i, data in enumerate(tig):
            if i > 10:
                break
            ll.append(data)
        pad_collate(ll)

    def test_get_dataset(self):

        lan_dic = {"C": 0,
                   "C#": 1,
                   "C++": 2,
                   "Go": 3,
                   "Java": 4,
                   "Javascript": 5,
                   "Lua": 6,
                   "Objective-C": 7,
                   "Python": 8,
                   "Ruby": 9,
                   "Rust": 10,
                   "Shell": 11}
        train, valid = get_data_set(lan_dic, load=False, no_file_length=False, debug=True)

    def test_repickle(self):
        repickle(pkl_dir=Path("C:/temp"), debug=True)
        repickle_vocab_pickle(debug=True)