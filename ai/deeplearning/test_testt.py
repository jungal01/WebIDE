from ai.deeplearning.testt import *
import unittest

class TesttTest(unittest.TestCase):
    def test_main_test(self):
        dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
        file = Path(dir_path.parent / "testfile")
        model, lookup = get_model_lookup()
        persistent_test(model, lookup, file)
        main_test(file)