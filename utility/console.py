# coding=utf-8
import re

import click
from tqdm import tqdm


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.argument('ip-scope')
def netbox_ipam_patch(ip_scope: str):
    """
    Scan a network and add them to NetBox

    IP_SCOPE example: 192.168.0.0/24,192.168.1.0/24,... (use , as the separator)
    """

    from helpers.configuration import Configuration
    from tasks.networkscan import ScanNetwork
    from tasks.patch_netbox import PatchNetbox, Args

    ip_scopes = list(x.strip(' ') for x in ip_scope.split(','))
    ip_scopes = list(x for x in ip_scopes if x)

    for target_ip_scope in ip_scopes:
        if not re.match(
            r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,3}$',
            target_ip_scope,
        ):
            click.echo(f'IP_SCOPE ({target_ip_scope}) must be a ip must with a subnet', err=True)
            return

    scan_network_result = dict()
    for target_ip_scope in tqdm(ip_scopes, desc='Scanning network'):
        tqdm.write(f'=== {target_ip_scope} ===')
        buffer = ScanNetwork(target_ip_scope)

        for ip, row in buffer.items():
            tqdm.write(f'  {ip}: {row.hostname}')

        scan_network_result.update(buffer)

    click.echo('Updating NetBox')
    PatchNetbox(Configuration.NetBox.base_url, Configuration.NetBox.api_token, [Args(
        ip=x.ip,
        dns_name=x.hostname,
    ) for x in scan_network_result.values()])


if __name__ == '__main__':
    cli()
