import argparse

from argparse import ArgumentParser, Namespace

def parse_args(sys_args: list['str']) -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog = 'Out-of-Band Configuration Script',
        description = 'Script for configuring iLO 5, iDRAC 9, and XCC interfaces'
    )

    parser.add_argument('-i', '--ip_address',       help = 'Specify a static IP address to set.')
    parser.add_argument('-n', '--hostname',         help = 'Specify the hostname to set.')
    parser.add_argument('-s', '--subnet_mask',      help = 'Specify the subnet mask to set (dotted decimal or CIDR).')
    parser.add_argument('-g', '--default_gateway',  help = 'Specify the default gateway to set.')
    parser.add_argument('-d', '--domain_name',      help = 'Specify the domain name to set.')
    parser.add_argument('-u', '--username',         help = 'Specify the administrator username to set.')
    parser.add_argument('-p', '--password',         help = 'Specify the administrator password to set.')

    parser.add_argument('--debug',                  help = 'Start the script in debug mode.', action='store_true')
    parser.add_argument('--default_ip',             help = 'Override the default IP address.')
    parser.add_argument('--default_suffix',         help = 'Override the default hostname suffix.')
    parser.add_argument('--increment_ip',           help = 'Increment the default IP address after each configuration.', action='store_true')
    parser.add_argument('--no_confirm',             help = 'Don\'t prompt to confirm the current configuration', action='store_true')

    return parser.parse_args()

def update_default_config(default_config: dict, args: Namespace) -> dict:
    updated_config: dict = default_config | {
        'current_ip': args.ip_address,
        'current_hostname': args.hostname,
        'subnet_mask': args.subnet_mask,
        'default_gateway': args.default_gateway,
        'domain_name': args.domain_name,
        'username': args.username,
        'password': args.password,
        'ilo_ip': args.default_ip or default_config['ilo_ip'],
        'hostname_suffix': args.default_suffix or default_config['hostname_suffix'],
        'confirm': not bool(args.no_confirm),
        'debug': not bool(args.debug),
        'increment_ip': bool(args.increment_ip)
    }

    return updated_config