#!/usr/bin/env bash
echo "This may take a while to build, as it requires some large packages get installed."
echo "This will install to the current directory and will add directories to your PATH."
echo "Continue?"
read  -n 1 -p ">" yn
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
  cargo build rust-build
  pip3 install --user flask
  pip3 install --user json

else
  echo "aborting..."
fi
