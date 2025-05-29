from getpass import getpass
from typing import Callable
from utils.ip import is_valid_ip, is_valid_subnet_mask, get_gateway_validator, get_subnet_mask, get_default_gateway

def confirm(confirm_prompt: str = '') -> bool:
    user_response = input(confirm_prompt).lower().strip()
    affirmative_responses = ['yes', 'ye', 'y']
    negative_responses = ['no', 'n']
    response_is_positive: bool = bool(user_response in affirmative_responses)
    response_is_negative: bool = bool(user_response in negative_responses)
    invalid_response_prompt: str = 'Invalid response, please enter \'y\' or \'n\': '

    return True if response_is_positive else False if response_is_negative else confirm(confirm_prompt = invalid_response_prompt)

def prompt(
        prompt_text: str, 
        error_message: str = '', 
        validate: bool | Callable = False, 
        formatter: bool | Callable = False, 
        password: bool = False, 
        default: str = '') -> str:
    user_input: str = input(prompt_text).strip() if not password else getpass(prompt_text).strip()
    if user_input == '' and bool(default):
        return default
    if not bool(validate) or validate(user_input):
        if bool(formatter):
            return formatter(user_input)
        return user_input
    else:
        if bool(error_message):
            print(error_message)
        return prompt(prompt_text, error_message, validate, formatter, password, default)

def prompt_for_config(config: dict) -> None:
    print('Welcome to the iLO configuration script!')
    config['current_ip'] = prompt(
        'Please enter the static IP to set for the iLO: ', 
        'Invalid IP, please try again.', validate = is_valid_ip).strip()
    config['current_hostname'] = prompt('Please enter the hostname to set for the iLO: ')
    config['subnet_mask'] = prompt(
        'Please enter the subnet mask to set for the iLO: ',
        'Invalid subnet mask, please try again.', 
        validate = is_valid_subnet_mask, 
        formatter = get_subnet_mask)
    gateway_guess: str = get_default_gateway(config['current_ip'], config['subnet_mask'])
    config['default_gateway'] = prompt(
        f'Please enter the default gateway to set for the iLO (press Enter to use {gateway_guess}): ',
        'Invalid default gateway, please try again', 
        validate = get_gateway_validator(config['current_ip'], config['subnet_mask']),
        default = gateway_guess)
    config['domain_name'] = prompt('Please enter the domain name to set for the iLO: ')
    config['username'] = prompt('Please enter the username to set for the iLO: ')
    #todo: password confirm
    config['password'] = prompt('Please enter the password to set for the iLO: ', password = True)
