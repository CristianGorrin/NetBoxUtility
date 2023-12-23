# coding=utf-8
import dataclasses
import socket
import typing

from networkscan import Networkscan


@dataclasses.dataclass(frozen=True)
class Record:
    ip: str
    hostname: typing.Optional[str]


def ScanNetwork(ip_and_prefix: str):
    """
    Scan a network and do a reverse dns lookup

    :param ip_and_prefix: Example 192.168.0.0/24
    :return: ip => Record
    """

    cidr_mask = ip_and_prefix.split('/')[1]

    scan = Networkscan(ip_and_prefix)
    scan.run()

    result: typing.Dict[str, Record] = dict()
    for address in scan.list_of_hosts_found:
        if address in result:
            continue

        dns_name = socket.getnameinfo((address, 0), 0)[0]
        if dns_name == address:
            dns_name = None

        result[address] = Record(
            ip=f'{address}/{cidr_mask}',
            hostname=dns_name,
        )

    return result
