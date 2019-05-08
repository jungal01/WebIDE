from ai.deeplearning.preprocessing import *
import unittest

class PreprocessingTest(unittest.TestCase):
    def test_generate_dictionary(self):
        generate_dictionary(debug=True)

    def test_select_vocabulary(self):
        select_vocabulary()