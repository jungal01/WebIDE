#!/usr/bin/env bash
echo "This may take a while to build, as it requires some large packages get installed."
echo "This will add directories to your PATH. Continue?"
read  -n 1 -p "[y/n]>" yn
echo

if [[ "$yn" = "y" ]]; then
  sudo dpkg -i cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb
  sudo apt-key add /var/cuda-repo-<version>/7fa2af80.pub
  sudo apt update
  sudo apt upgrade -y
  sudo apt-get install cuda
  git clone https://github.com/juj/emsdk.git
  cd emsdk
  ./emsdk install latest
  ./emsdk activate latest
  source ./emsdk_env.sh
  cd ..
  curl -sf -L https://static.rust-lang.org/rustup.sh | sh
  echo 'export PATH=.:~/.cargo/bin:$PATH' >> ~/.bashrc
  source ~/.bashrc
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
