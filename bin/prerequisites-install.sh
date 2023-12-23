#!/usr/bin/env bash
set -e

START=$(date +%s)

handle_error() {
    echo "An error occurred. Exiting..."
    popd
    exit 1
}

trap handle_error ERR

pushd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.." > /dev/null

echo "=== Git submodule ==="
echo "This can take a while..."
git submodule init
git submodule update

echo "=== Dependencies ==="
sudo apt install -y build-essential

echo "=== Install Python 3.11  ==="
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install -y python3.11 python3.11-dev python3.11-venv

END=$(date +%s)
echo "Done efter $(($END-$START)) seconds"
popd > /dev/null
