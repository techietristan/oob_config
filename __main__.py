from argparse import Namespace
from sys import argv
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from utils.args import parse_args, update_default_config
from utils.config_network import config_network
from utils.config_session import config_session
from utils.create_user import create_user
from utils.hostname import get_next_hostname, set_hostname
from utils.ip import get_next_ip
from utils.login import login
from utils.logout import logout
from utils.ping import wait_for_ping
from utils.prompts import confirm, prompt_for_config, confirm_config
from utils.reset import reset_ilo
from utils.sys import exit_with_code

disable_warnings(InsecureRequestWarning)

default_config: dict = {
    'ilo_ip': '169.254.1.2',
    'ilo_username': 'Administrator',
    'ilo_headers': { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Connection': 'keep-alive' },
    'hostname_suffix': '-r',
    'enforce_case': 'lower',
    'hosts_in_series': 0,
    'session_uri': '',
    'token': '',
}

def main(config: dict = {}) -> None:
    args: Namespace = parse_args(argv)
    config: dict = update_default_config(default_config, args)
    ilo_ip: str = config['ilo_ip']
    try:
        if not bool(config['current_ip']):
            prompt_for_config(config)
        if bool(config['confirm']) and confirm_config(config):
            if not wait_for_ping(ilo_ip):
                if confirm(f'Unable to reach the iLO at {ilo_ip}. Do you want to try again?'):
                    return main(config)
            #todo: show config status
            login_response: Response = login(config)
            config_session(config, login_response)
            create_user(config)
            config_network(config)
            set_hostname(config)
            reset_ilo(config)
        else:
            print('\nExiting script.')
            exit_with_code(0)
        config['current_ip'] = get_next_ip(config['current_ip'])
        config['current_hostname'] = get_next_hostname(config, config['current_hostname'])
        
        return main(config)
    except KeyboardInterrupt:
        print('\nKeyboard interrupt received, exiting script.')
        exit_with_code(130)

if __name__ == '__main__':
    main()
