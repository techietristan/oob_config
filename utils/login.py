import requests

from getpass import getpass
from requests import Response

def login(config: dict) -> Response:

    ilo_ip, ilo_headers, ilo_username = config['ilo_ip'], config['ilo_headers'], config['ilo_username']
    ilo_password: str = getpass('Please enter the password for the currently connected iLO: ')
    login_payload: dict = {'Password': ilo_password, 'UserName': ilo_username}
    login_url: str = f'https://{ilo_ip}/redfish/v1/Sessions/'

    response: Response = requests.post(login_url, headers = ilo_headers, json = login_payload, verify = False)
    
    if bool(config['debug']):
        print(response.status_code, response.text, response.headers)

    return response