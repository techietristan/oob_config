import requests
from requests import Response

def reset_ilo(config: dict) -> Response:
    ilo_ip, ilo_headers, token = config['ilo_ip'], config['ilo_headers'], config['token']
    reset_url: str = f'https://{ilo_ip}/json/ilo_status'
    reset_payload: dict = {
        'cause': 'config',
        "method": "reset_ilo",
        'session_key': token
    }

    return requests.post(reset_url, headers = ilo_headers, json = reset_payload, verify = False)