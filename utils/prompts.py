from getpass import getpass
from typing import Callable
from utils.ip import is_valid_ip

def confirm(confirm_prompt: str = '', error = False) -> bool:
    prompt = format_red(confirm_prompt) if error else confirm_prompt
    user_response = input(prompt).lower().strip()
    affirmative_responses = ['yes', 'ye', 'y']
    negative_responses = ['no', 'n']
    response_is_positive: bool = bool(user_response in affirmative_responses)
    response_is_negative: bool = bool(user_response in negative_responses)
    invalid_response_prompt: str = 'Invalid response, please enter \'y\' or \'n\': '

    return True if response_is_positive else False if response_is_negative else confirm(confirm_prompt = invalid_response_prompt)

def prompt(prompt_text: str, error_message: str = '', validate: bool | Callable = False, password: bool = False, default: str = '') -> str:
    user_input: str = input(prompt_text) if not password else getpass(prompt_text)
    if user_input == '' and bool(default):
        return default
    if not bool(validate):
        return user_input
    if validate(user_input):
        return user_input
    else:
        if bool(error_message):
            print(error_message)
        return prompt(prompt_text, error_message, validate)

def prompt_for_config(config: dict) -> None:
    print('Welcome to the iLO configuration script!')
    config['current_ip'] = prompt(
        'Please enter the static IP to set for the iLO: ', 
        'Invalid IP, please try again.', is_valid_ip)
    config['current_hostname'] = prompt('Please enter the hostname to set for the iLO: ')
    #todo: cidr & subnet validation
    config['subnet_mask'] = prompt('Please enter the subnet mask to set for the iLO: ')
    #todo: gateway default function
    config['default_gateway'] = prompt('Please enter the default gateway to set for the iLO: ')
    config['domain_name'] = prompt('Please enter the domain name to set for the iLO: ')
    config['username'] = prompt('Please enter the username to set for the iLO: ')
    config['password'] = prompt('Please enter the password to set for the iLO: ', password = True)
