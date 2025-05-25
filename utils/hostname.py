import re
import requests

from re import Match
from requests import Response

def set_hostname(config: dict) -> Response:
    ilo_ip, ilo_headers, token = config['ilo_ip'], config['ilo_headers'], config['token']
    hostname_url: str = f'https://{ilo_ip}/json/network_general'
    current_hostname_config: dict = requests.get(hostname_url, headers = ilo_headers, verify = False).json()
    hostname_payload: dict = current_hostname_config | {
        'dns_name': config['hostname'],
        'domain_name': config['domain_name'],
        'method': 'set_general',
        'session_key': token
    }

    return requests.post(hostname_url, headers = ilo_headers, json = hostname_payload, verify = False)

def get_next_letter(config: dict, hostname: str) -> str:
    alphabet: list[str] = list('abcdefghijklmnopqrstuvwxyz')
    hosts_in_series: int = config['hosts_in_series']
    final_char: str = hostname[-1]
    if final_char.isdigit():
        return ''
    else:
        current_letter_index: int = alphabet.index(final_char)
        host_is_last_in_series: bool = bool(current_letter_index + 1 == hosts_in_series)
        next_letter_index: int = 0 if host_is_last_in_series else current_letter_index + 1
        next_letter: str = alphabet[next_letter_index]
        return next_letter

def get_next_hostname(config: dict, current_hostname: str) -> str:
    hostname_suffix: str = config['hostname_suffix']
    stripped_hostname: str = current_hostname.strip().strip(hostname_suffix).lower()
    next_letter: str = get_next_letter(config, stripped_hostname)
    base_hostname: str = stripped_hostname[:-1] if bool(next_letter) else stripped_hostname
    final_digits_match: Match = re.search(r'(\d+$)', base_hostname)
    final_digits: str = final_digits_match.group()
    final_digits_start: int = final_digits_match.span()[0]
    final_digits_length: int = len(final_digits)        
    hostname_prefix: str = stripped_hostname[:final_digits_start]
    next_digits: int = int(final_digits) + 1
    padded_next_digits: str = str(next_digits).zfill(final_digits_length) if next_letter in ['', 'a'] else final_digits
    next_hostname: str = f'{hostname_prefix}{padded_next_digits}{next_letter}{hostname_suffix}'

    return next_hostname