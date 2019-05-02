from ai.deeplearning.testt import persistent_test, main_test, get_model_lookup
from pathlib import Path
import os

# go to the function definition file for an example.
def identify(file):
    raise DeprecationWarning("This interface is obsolete. Use persistent_identify() with prepare_model_lookup()")
    return main_test(file)

def persistent_identify(model, lookup, file):
    return persistent_test(model, lookup, file)

def prepare_model_lookup():
    return get_model_lookup()

if __name__=="__main__":
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    file=Path(dir_path/"ai"/"testfile")
    main_test(file)
