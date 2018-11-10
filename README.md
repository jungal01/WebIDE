# WebIDE

This is version 1.0.0 of WebIDE, Designed by Allen Junge, Kevin Cobble, Eros Casas, and Jason Hu.

# Setting Up

1. run `build-project.sh`
   * This will install emscripten and Rust stable, and add both to your $PATH.
   * It also adds the Rust packages `cargo-web` and `wasm-gc`.
   * For python, it will create the venv `webide` and install `Flask`, `torch`, `numpy`, and `pathlib`.
2. run `app.py` with python 3.5 or later
3. navigate to 0.0.0.0:5000/

## For our professor:

  This is all of our collaborative work on the alpha version, for you to test and look through.
  currently, only C and C++ are available to both compile and run in the browser, and Rust
  can only compile to WebAssembly and linux binaries. At the moment, the output box will only
  display errors, and successfully compiled code will get displayed in the browser console.
  The AI is functional, but the code to call it is a work in progress.
