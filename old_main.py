# coding=utf-8
import csv
import socket

from networkscan import Networkscan
from netbox import NetBox
from netbox.exceptions import NotFoundException
from tqdm import tqdm


CONF_PATH_CSV = '/home/netbox/Downloads/netbox.csv'
CONF_SCOPES = ['10.254.0.0/24']
CONF_NET_BOX = dict({
    'host': '192.168.43.129',
    'port': 80,
    'use_ssl': False,
    'auth_token': '51aa99ec5fa6c48ffadd00287532053c5bba6018',
})


def Main():
    update_args = LoadDescription()
    addresses = GetAddresses()

    found_address = UpdateAddress(addresses, update_args)
    with open('not_found_dns.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['address', 'description'])
        writer.writeheader()

        for addr, info in update_args.items():
            if addr not in found_address:
                writer.writerow(dict({
                    'address': addr,
                    'description': info['description'] if 'description' in info else '',
                }))


def GetAddresses() -> set:
    addresses = set()

    for scope in CONF_SCOPES:
        print(f'Networkscan: {scope}')
        my_scan = Networkscan(scope)
        my_scan.run()

        for address in my_scan.list_of_hosts_found:
            addresses.add(address)

    return addresses


def LoadDescription() -> dict:
    update_args = dict()

    offset = 0
    with open(CONF_PATH_CSV) as file:
        for line in csv.DictReader(file):
            offset += 1
            try:
                address_val = '.'.join([str(int(x)) for x in line["address"].split('.')])
                update_args[address_val] = {
                    'description': line['description'],
                    'dns_name': line['dns_name'],
                }

            except Exception as e:
                raise Exception(f'Csv line #{str(offset)}: {line["address"]} => {str(e)}') from e

    return update_args


def UpdateAddress(addresses, update_args) -> list:
    netbox_cli = NetBox(**CONF_NET_BOX)
    found_address = list()

    for address in tqdm(sorted(addresses), desc='Ip address'):
        found_address.append(address)
        # @see https://docs.ansible.com/ansible/latest/collections/netbox/netbox/netbox_ip_address_module.html
        #   Parameter "data" use for args values (skip address)
        args = dict() if address not in update_args else update_args[address]

        dns_name = args['dns_name'].lstrip('') if 'dns_name' in args else ''

        if not dns_name:
            try:
                dns_name = socket.getnameinfo((address, 0), 0)[0]
                if dns_name != address:
                    args['dns_name'] = dns_name

            except Exception:
                pass

        tqdm.write(f'{address} -- {str(args)}')
        try:
            netbox_cli.ipam.update_ip(address, **args)

        except NotFoundException:
            netbox_cli.ipam.create_ip_address(address, **args)

    return found_address


if __name__ == '__main__':
    Main()
