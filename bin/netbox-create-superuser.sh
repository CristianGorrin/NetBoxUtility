#!/usr/bin/env bash
set -e

handle_error() {
    echo "An error occurred. Exiting..."
    popd
    exit 1
}

trap handle_error ERR

pushd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.." > /dev/null

cd netbox-docker
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser

popd > /dev/null
