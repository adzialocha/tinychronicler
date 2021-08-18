# Install dependencies for pillow
sudo apt-get install libjpeg-dev

# Install dependencies required to install llvmlite
sudo apt-get install llvm-9

# Install dependencies required to build scipy
sudo apt-get install gfortran libopenblas-dev liblapack-dev libatlas3-base libgfortran5

# Clone tinychronicler repository
git clone https://github.com/adzialocha/tinychronicler
cd tinychronicler

# Install all dependencies
LLVM_CONFIG=llvm-config-9 poetry install

# Start tinychronicler server
poetry run python tinychronicler

# @TODO
# HiFi Berry steps?
# https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/

# Install pure data
# See: http://pi.bek.no/pdinstall/
sudo apt-get install puredata

# @TODO
# Setup auto-starting program on boot
# See: http://pi.bek.no/autostartProgramOnBoot/
