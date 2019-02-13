# WebIDE

This is version 1.1.0 of WebIDE, Designed by Allen Junge, Kevin Cobble, Eros Casas, and Jason Hu.

# Setting Up

1. run `build-project.sh`
  * This will install emscripten and Rust stable, and add both to your $PATH.
  * It also adds the Rust packages `cargo-web` and `wasm-gc`.
  * For python, it will create the venv `webide` and install `Flask`, `torch`, `numpy`, and `pathlib`.
2. run `app.py` with python 3.5 or later
3. navigate to 0.0.0.0:5000/

## For our professor:

  This is all of our collaborative work on the beta version, for you to test and look through.
  currently, only C and C++ are available to both compile and run in the browser, and Rust will only compile natively on linux. At the moment, the output box will only
  display errors, and the functional AI has a <b>strong</b> preference to Java at the moment, so even perfectly functional code will get misidentified and receive our
  `language support` error.


## Schedule for 2019 Spring
syntax highlighting - AJ & KC & EC - start by 2-28
config file - select compile options - AJ & EC - start by 2-25
downloading/uploading files and folders - KC & EC - Complete 3-1
setup apache server - contact adam/helpdesk
redirection warnings - AJ & EC & KC- complete by  2-25
tabs - KC & EC - Complete by 2-25
multiplatform compilation
[current]
ui
ai - JH
code migration - KC - Complete by 2-17
