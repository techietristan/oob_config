import requests
from requests import Response

def config_network(config: dict) -> Response:
    ilo_ip, ilo_headers, token = config['ilo_ip'], config['ilo_headers'], config['token']
    ipv4_url: str = f'https://{ilo_ip}/json/network_ipv4'
    current_ipv4_url: str = f'{ipv4_url}/interface/0'
    current_ipv4_config: dict = requests.get(current_ipv4_url, headers = ilo_headers, verify = False).json()
    ipv4_payload: dict = current_ipv4_config | {
        'dhcp_enabled': 0,
        'ip_address': '100.102.57.33',
        'subnet_mask': '255.255.255.0',
        'gateway_ip_address': '100.102.57.1',
        "method": "set_ipv4",
        'session_key': token
    }

    response: Response = requests.post(ipv4_url, headers = ilo_headers, json = ipv4_payload, verify = False)

    if bool(config['debug']):
        print(response.status_code, response.text, response.headers)

    return response