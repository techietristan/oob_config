import requests

from requests import Response

def logout(config: dict) -> Response:

    logout_url, ilo_headers = config['session_uri'], config['ilo_headers']
    
    response: Response = requests.delete(logout_url, headers = ilo_headers, verify = False)

    if bool(config['debug']):
        print(response.status_code, response.text, response.headers)

    return response