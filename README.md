# (optional) Netbox dev server
_This assumes that docker is installed_

NetBox is built with: https://github.com/netbox-community/netbox-docker

1) Install by
```bash
./bin/netbox-install.sh
```
2) Create file `./netbox-docker/docker-compose.override.yml` with (replace {exposed_port}):
```yaml
version: '3.4'
services:
  netbox:
    ports:
      - {exposed_port}:8080
```
3) Start Netbox:
```bash
./bin/netbox-start.sh
```
4) Create a new superuser:
```bash
./bin/netbox-create-superuser.sh
```

# Utility
To install all the prerequisites, run:
```bash
./bin/prerequisites-install.sh
```


1) Install by
```bash
./bin/utility-install.sh
```
2) Create a configuration file in `utility/configuration.yaml` with this format:
```yaml
NetBox:
  base_url: http://127.0.0.1:8000
  api_token: bde32ac44b7226452aa3c8dc266c88f07711ff32
```

_List commands:_
```bash
./bin/utility-console.sh
```

_Help text:_
```text
Add --help to a command, this will display help text:

$./bin/utility-console.sh netbox-ipam-patch --help
Usage: console.py netbox-ipam-patch [OPTIONS] IP_SCOPE

  Scan a network and add it to NetBox

  192.168.0.0/24 (IP_SCOPE example)

Options:
  --help  Show this message and exit.
```
