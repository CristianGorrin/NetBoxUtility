# coding=utf-8
import dataclasses
import typing

from netbox_python import NetBoxClient


@dataclasses.dataclass(frozen=True)
class Args:
    # @see https://docs.ansible.com/ansible/latest/collections/netbox/netbox/netbox_ip_address_module.html
    ip: str

    dns_name: typing.Optional[str]

    def ToNetBox(self):
        result = dict({'address': self.ip})

        if self.dns_name is not None:
            result['dns_name'] = self.dns_name

        return result


def PatchNetbox(
    netbox_url: str,
    netbox_api_token: str,
    args: typing.List[Args]
):
    nb = NetBoxClient(base_url=netbox_url, token=netbox_api_token)

    existing_ips = dict({
        x['address']: x
        for x in nb.ipam.ip_addresses.all().data
    })

    if create := [x for x in args if x.ip not in existing_ips]:
        nb.ipam.ip_addresses.create([x.ToNetBox() for x in create])

    update = []
    for row in args:
        if existing := existing_ips.get(row.ip):
            data = row.ToNetBox()
            data['id'] = existing['id']

    if update:
        nb.ipam.ip_addresses.update(update)
