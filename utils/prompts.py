from getpass import getpass
from typing import Callable
from utils.hostname import format_hostname
from utils.ip import is_valid_ip, is_valid_subnet_mask, get_gateway_validator, get_subnet_mask, get_default_gateway

def confirm(confirm_prompt: str = '') -> bool:
    user_response = input(confirm_prompt).lower().strip()
    affirmative_responses = ['yes', 'ye', 'y']
    negative_responses = ['no', 'n']
    response_is_positive: bool = bool(user_response in affirmative_responses)
    response_is_negative: bool = bool(user_response in negative_responses)
    invalid_response_prompt: str = 'Invalid response, please enter \'y\' or \'n\': '

    return True if response_is_positive else False if response_is_negative else confirm(confirm_prompt = invalid_response_prompt)

def get_password(prompt_text: str) -> str:
    password: str = getpass(prompt_text).strip()
    password_confirm: str = getpass('Please enter the password again: ').strip()
    if bool(password == password_confirm):
        return password
    else:
        print('Passwords do not match, please try again.')
        return get_password(prompt_text)

def prompt_and_update(config: dict,
        config_item: str,
        prompt_text: str, 
        error_message: str = '', 
        validate: bool | Callable = False, 
        formatter: bool | Callable = False, 
        password: bool = False, 
        default: str = '') -> None:
    if bool(config[config_item]):
        user_input: str = config[config_item].strip()
    elif bool(password):
        user_input: str = get_password(prompt_text)
    else:
        user_input: str = input(prompt_text).strip()
    if user_input == '' and bool(default):
        config[config_item] = default
        return
    if not bool(validate) or validate(user_input):
        if bool(formatter):
            config[config_item] = formatter(config, user_input)
            return
        else:
            config[config_item] = user_input
            return
    else:
        if bool(error_message):
            print(error_message)
        return prompt(config, config_item, prompt_text, error_message, validate, formatter, password, default)

def prompt_for_config(config: dict) -> None:
    print('Welcome to the Out-of-Band configuration script!')
    prompt_and_update(config, 'current_ip', 
        'Please enter the static IP to set for the iLO: ', 
        'Invalid IP, please try again.', validate = is_valid_ip)
    prompt_and_update(config, 'current_hostname', 
        'Please enter the hostname to set for the iLO: ',
        formatter = format_hostname)
    prompt_and_update(config, 'subnet_mask', 
        'Please enter the subnet mask to set for the iLO (dotted decimal or CIDR format): ',
        'Invalid subnet mask, please try again.', 
        validate = is_valid_subnet_mask, 
        formatter = get_subnet_mask)
    gateway_guess: str = get_default_gateway(config['current_ip'], config['subnet_mask'])
    is_valid_gateway: Callable = get_gateway_validator(config['current_ip'], config['subnet_mask'])
    prompt_and_update(config, 'default_gateway', 
        f'Please enter the default gateway to set for the iLO (press Enter to use {gateway_guess}): ',
        'Invalid default gateway, please try again', 
        validate = is_valid_gateway,
        default = gateway_guess)
    prompt_and_update(config, 'domain_name', 'Please enter the domain name to set for the iLO: ')
    prompt_and_update(config, 'username', 'Please enter the username to set for the iLO: ')
    prompt_and_update(config, 'password', 'Please enter the password to set for the iLO: ', password = True)

def confirm_config(config: dict) -> bool:
    print(f'\nDo you want to push the following config to the currently connected iLO?\n\n\t',
    f'Static IP: {config['current_ip']}\n\t',
    f'Hostname: {config['current_hostname']}\n\t',
    f'Subnet Mask: {config['subnet_mask']}\n\t',
    f'Default Gateway: {config['default_gateway']}\n\t',
    f'Domain: {config['domain_name']}\n\t',
    f'Username: {config['username']}\n\t')
    
    return confirm('(y or n): ')
