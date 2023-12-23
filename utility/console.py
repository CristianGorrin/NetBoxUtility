# coding=utf-8
import re

import click


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.argument('ip-scope')
def netbox_ipam_patch(ip_scope: str):
    """
    Scan a network and add them to NetBox

    IP_SCOPE 192.168.0.0/24 (example)
    """

    if not re.match(
        r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,3}$',
        ip_scope,
    ):
        click.echo('Value must be a ip must with a subnet', err=True)
        return

    from helpers.configuration import Configuration

    from utility.tasks.networkscan import ScanNetwork
    click.echo('Scanning network')
    scan_network_result = ScanNetwork(ip_scope)

    from utility.tasks.patch_netbox import PatchNetbox, Args
    click.echo('Updating NetBox')
    PatchNetbox(Configuration.NetBox.base_url, Configuration.NetBox.api_token, [Args(
        ip=x.ip,
        dns_name=x.hostname,
    ) for x in scan_network_result.values()])


if __name__ == '__main__':
    cli()
