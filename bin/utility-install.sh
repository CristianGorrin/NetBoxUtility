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
cd utility

echo "=== Python venv ==="
[ ! -d "./venv" ] && python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install setuptools
pip install wheel
pip install -r ./requirements.txt
deactivate

END=$(date +%s)
echo "Done efter $(($END-$START)) seconds"
popd > /dev/null
