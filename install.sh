#!/bin/bash
set -e
echo "Welcome to the PiFmTx-neo installer!"

echo "=== Updating system packages ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing dependencies ==="
sudo apt install -y ffmpeg git build-essential curl pkg-config libssl-dev libsndfile1-dev
pip install ffmpeg-python PySSTV numpy flask click Pillow --break-system-packages

echo "=== Detecting Raspberry Pi model ==="
PI_MODEL=$(tr -d '\0' < /proc/device-tree/model)
echo "Detected model: $PI_MODEL"

REPO_DIR="$HOME/PiFmRds"
if [ ! -d "$REPO_DIR" ]; then
    echo "Cloning PiFM-RDS repository..."
    git clone https://github.com/ChristopheJacquet/PiFmRds.git "$REPO_DIR"
fi

SRC_DIR="$REPO_DIR/src"
cd "$SRC_DIR" || { echo "ERROR: Failed to enter repository src directory"; exit 1; }

if [[ "$PI_MODEL" == *"Zero 2 W"* ]]; then
    if [ -f Makefile ]; then
        echo "Patching Makefile for Zero 2 W (RPI_VERSION=3)"
        sed -i 's/^RPI_VERSION :=.*/RPI_VERSION = 3/' Makefile
    else
        echo "ERROR: Makefile not found in src! Cannot patch."
        exit 1
    fi
fi

sed -i 's/^ARCH_CFLAGS.*$/ARCH_CFLAGS = -march=armv7-a -O3 -mtune=arm1176jzf-s -mfloat-abi=hard -mfpu=vfp -ffast-math/' Makefile
sed -i 's/^TARGET = .*$/TARGET = 3/' Makefile

echo "=== Compiling PiFM-RDS... ==="
make clean
make

echo "=== Installing PiFM-RDS to PATH... ==="
sudo cp pi_fm_rds /usr/local/bin/
sudo chmod +x /usr/local/bin/pi_fm_rds

APP_TX_DIR="$HOME/pifmtx-neo/pifmtx-neo/"
APP_REPO_URL="https://github.com/NotHavocc/pifmtx-neo"

if [ ! -d "$RUST_TX_DIR" ]; then
    echo "=== Cloning PiFmTx-neo repository... ==="
    git clone "$APP_REPO_URL" "$APP_TX_DIR"
fi

cd "$APP_TX_DIR" || { echo "ERROR: Failed to enter PiFmTx-neo directory"; exit 1; }

while true; do
    read -p "Would you like to add PiFmTx-neo to PATH? (Y/N) " yn
    case $yn in
        [Yy]* ) chmod +x pifmtx-neo.py; sudo ln -s $(pwd)/pifmtx-neo.py /usr/local/bin/pifmtx-neo; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "=== Installation complete! ==="
echo "PiFM-RDS installed"
echo "PiFmTx-neo installed: /usr/local/bin/pifmtx-neo"
echo "You can now run:"
echo "  pifmtx-neo"
