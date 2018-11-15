#!/usr/bin/env bash
echo "This may take a while to build, as it requires some large packages get installed."
echo "This will add directories to your PATH. Continue?"
read  -n 1 -p "(y)es or (n)o>" yn
echo

if [[ "$yn" = "y" ]]; then
  sudo apt update
  sudo apt upgrade -y
  git clone https://github.com/juj/emsdk.git
  cd emsdk
  ./emsdk install latest
  ./emsdk activate latest
  source ./emsdk_env.sh
  cd ..
  curl -sf -L https://static.rust-lang.org/rustup.sh | sh
  echo 'export PATH=.:~/.cargo/bin:$PATH' >> ~/.bashrc
  rustup target add wasm32-unknown-unknown
  cargo install -f cargo-web
  cargo install --git https://github.com/alexcrichton/wasm-gc
  #cd rust-build
  #cargo build --release
  #cd ..
  python3 -m venv webide
  source webide/bin/activate
  pip3 install Flask torch numpy pathlib

else
  echo "aborting..."
fi
