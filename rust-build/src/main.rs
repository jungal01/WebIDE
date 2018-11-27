extern crate wasm_bindgen;

use wasm_bindgen::prelude::*;
use std::{env, fs};

fn main() {
  let arg: Vec<String> = env::args().collect();
  let filename = arg[1];
}
