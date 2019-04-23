from ai.deeplearning.testt import main_test
from pathlib import Path
import os

# go to the function definition file for an example.
def identify(file):
    return main_test(file)

if __name__=="__main__":
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    file=Path(dir_path/"ai"/"testfile")
    main_test(file)