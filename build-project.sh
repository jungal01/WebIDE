#!/usr/bin/env bash
echo
echo "This may take a while to build, as it requires some large packages get installed."
echo "It is highly recommended to run this script as su."
echo "This will modify bashrc to add directories to your PATH. Continue?"
read  -n 1 -p "[y/n/i]> " yni
echo

if [[ "$yni" = "y" ]]; then
  # install the CUDA version for ubuntu for the AI
  echo "installing CUDA"
  echo
  sudo dpkg -i cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb
  sudo apt-key add /var/cuda-repo-<version>/7fa2af80.pub
  sudo apt update
  sudo apt upgrade -y
  sudo apt-get install cuda
  # end cuda


  echo
  echo "updating Gnu Compiler Collection to 8.1"
  echo
  # update gcc to latest version
  sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
  sudo apt update && sudo apt upgrade -y
  sudo apt install gcc-8 g++-8 -y
  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-8
  # end gcc


  echo
  echo "installing programming languages"
  echo
  # language installations
  # gcc options
  sudo apt install gnat -y # ada
  sudo apt install gfortran -y # fortran
  sudo apt install gccgo -y # go
  sudo apt install gnustep-devel -y # obj c
  echo '. /usr/share/GNUstep/Makefiles/GNUstep.sh' >> ~/.bashrc

  #other languages
  # OpenJDK Java
  sudo add-apt-repository ppa:openjdk-r/ppa -y
  sudo apt update && sudo apt upgrade -y
  sudo apt install openjdk-11-jdk -y
  # end Java
  # Rust
  curl -sf -L https://static.rust-lang.org/rustup.sh | sh
  echo 'export PATH=.:~/.cargo/bin:$PATH' >> ~/.bashrc
  source ~/.bashrc
  # end Rust
  # Lua
  curl -R -O http://www.lua.org/ftp/lua-5.3.5.tar.gz
  tar zxf lua-5.3.5.tar.gz
  cd lua-5.3.5
  make install
  # end Lua
  sudo apt install ruby-full -y # ruby
  # python latest stable version
  sudo add-apt-repository ppa:deadsnakes/ppa -y
  sudo apt install python3.7 -y
  sudo apt install python3.6 -y
  # end python


  echo
  echo "installing alternative compilers"
  echo
  # Compilers
  # Clang
  sudo apt install build-essential xz-utils curl
  curl -SL http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-18.04.tar.xz | tar -xJC .
  mv clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-18.04 clang_7.0.1
  sudo mv clang_7.0.1 /usr/local
  echo 'export PATH=/usr/local/clang_7.0.1/bin:$PATH' >> ~/.bashrc
  echo 'export LD_LIBRARY_PATH=/usr/local/clang_7.0.1/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
  # end clang
  # Pypy
  sudo add-apt-repository ppa:pypy/ppa -y
  sudo apt install pypy3 -y
  # end pypy


  echo
  echo "installing non-linux platform options"
  echo
  # platform options
  # WebAssembly
  git clone https://github.com/juj/emsdk.git
  cd emsdk
  ./emsdk install latest
  ./emsdk activate latest
  source ./emsdk_env.sh
  cd ..
  # rust wasm
  rustup target add wasm32-unknown-unknown
  cargo install -f cargo-web
  cargo install --git https://github.com/alexcrichton/wasm-gc

  echo
  echo "setting up the Python server environment"
  echo
  # Creates the venv for python and installs python requirements
  python3.6 -m venv webide
  source webide/bin/activate
  pip install -r requirements.txt

  echo "Our job here is done. Go forth and fix bugs!"


elif [[ "$yni" = "i" ]]; then
  echo
  echo "this adds the following lines to bashrc:"
  echo 'export PATH=.:~/.cargo/bin:$PATH; . /usr/share/GNUstep/Makefiles/GNUstep.sh; export PATH=/usr/local/clang_7.0.1/bin:$PATH; export LD_LIBRARY_PATH=/usr/local/clang_7.0.1/lib:$LD_LIBRARY_PATH'
  echo
  echo "This adds the following ppa's:"
  echo 'ubuntu-toolchain-r/test; openjdk-r/ppa; deadsnakes/ppa; pypy/ppa'
  echo
  echo "This installs the following packages:"
  echo 'cuda-repo-ubuntu1804-10-0-local-10.0.130-410.48_1.0-1_amd64.deb; cuda; gcc-8; g++-8; gnat; gfortran; gccgo; gnustep-devel; openjdk-11-jdk; python3.7; python3.6; ruby-full, pypy3'
  echo
  echo "this downloads and installs the following from the web:"
  echo 'http://www.lua.org/ftp/lua-5.3.5.tar.gz; https://static.rust-lang.org/rustup.sh; http://releases.llvm.org/7.0.1/clang+llvm-7.0.1-x86_64-linux-gnu-ubuntu-18.04.tar.xz'
  echo
  echo "this clones and installs the following repositories:"
  echo 'https://github.com/juj/emsdk.git;'
  echo
  echo "this installs the following python packages:"
  cat requirements.txt
  echo
  echo "this installs the following Rust targets and packages:"
  echo 'wasm32-unknown-unknown; cargo-web; https://github.com/alexcrichton/wasm-gc;'


else
  echo "aborting"
fi
