import requests
from requests import Response

def create_user(config: dict) -> Response:
    ilo_ip, ilo_headers, token = config['ilo_ip'], config['ilo_headers'], config['token']
    accounts_url: str = f'https://{ilo_ip}/redfish/v1/AccountService/Accounts/'
    new_user_payload: dict = {
        'Oem': {
            'Hpe': {
                'LoginName': config['username'],
                'SkipEscCharsCheck': True,
                'ServiceAccount': False
            }
        },
        'UserName': config['username'],
        'Password': config['password'],
        'RoleId': 'Administrator'
    }

    response: Response = requests.post(accounts_url, headers = ilo_headers, json = new_user_payload, verify = False)

    if bool(config['debug']):
        print(response.status_code, response.text, response.headers)

    return response